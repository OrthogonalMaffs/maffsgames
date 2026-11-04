#!/usr/bin/env python3
# ci-line: Fraction input modes (default unchanged, whole and signed modes, keyboard/keypad, layout and planted faults) |
# ci-deps: scripts/fixtures/fraction-input.html schools/assets/fraction-input.js schools/assets/keypad.js schools/assets/answer.js
"""FRACTION-WHOLE: exercise the real component, including combinations and sign-dropping plants.

The expected raw strings and values below are fixed independently of the component. MaffsAnswer only
checks that its existing parser reads those strings; it does not supply the test's expected values.
"""
from pathlib import Path
import sys

from playwright.sync_api import sync_playwright
import bank_common as bc
import plant_common as pc

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'schools/assets/fraction-input.js'
FIXTURE = ROOT / 'scripts/fixtures/fraction-input.html'
PLANTS = [
    ('whole omitted', "if (whole) inputs.unshift(whole);", "if (false) inputs.unshift(whole);"),
    ('whole dropped from raw', "var raw = w && f ? w + ' ' + f : w || f;", "var raw = f;"),
    ('sign dropped from raw', "return raw && negative ? '-' + raw : raw;", "return raw;"),
    ('sign typing ignored', "if (sign && el.value.indexOf('-') !== -1) toggleSign();", "if (false) toggleSign();"),
    ('compact whole width broken', "'.mfi-sign{cursor:pointer}',", "'.mfi-sign{cursor:pointer}', '.mfi-parts>.mfi-in{width:12rem}',"),
]


def check(page, script):
    page.set_content(FIXTURE.read_text(encoding='utf-8'))
    page.add_script_tag(content=(ROOT / 'schools/assets/answer.js').read_text(encoding='utf-8'))
    page.add_script_tag(content=(ROOT / 'schools/assets/keypad.js').read_text(encoding='utf-8'))
    page.add_script_tag(content=script)
    return page.evaluate(r"""() => {
      const errors = [], host = document.getElementById('host');
      const eq = (a,b,what) => { if (JSON.stringify(a)!==JSON.stringify(b)) errors.push(what+': '+JSON.stringify(a)+' != '+JSON.stringify(b)); };
      const type = (el, v) => { el.value=v; el.dispatchEvent(new Event('input', {bubbles:true})); };
      for (const whole of [false,true]) for (const signed of [false,true]) {
        const f=MaffsFractionInput.mount(host,{whole,signed}), tag=JSON.stringify({whole,signed});
        const n=f.inputs[whole?1:0], d=f.inputs[whole?2:1], w=whole?f.inputs[0]:null;
        eq(f.inputs.length,whole?3:2,tag+' input count');
        if(f.inputs.length!==(whole?3:2)) continue;
        eq(f.raw(),'','empty'); eq(f.value(),null,'empty value'); eq(f.filled(),false,'empty filled');
        eq(host.querySelectorAll('button').length,signed?1:0,'button count');
        type(n,'3'); type(d,'4'); if(w) type(w,'2');
        const positive=whole?'2 3/4':'3/4';
        eq(f.raw(),positive,tag+' positive raw'); eq(f.filled(),true,'filled');
        eq(f.value(),whole?{num:3,den:4,whole:2}:{num:3,den:4},'positive value');
        if(signed) {
          const sign=host.querySelector('button');
          eq(sign.getAttribute('aria-label'),'Make negative','positive label');
          eq(sign.getBoundingClientRect().left < f.inputs[0].getBoundingClientRect().left,true,'sign before whole or fraction');
          sign.click(); eq(sign.textContent,'−','negative button'); eq(sign.getAttribute('aria-label'),'Make positive','negative label');
          eq(sign.getAttribute('aria-pressed'),'true','negative pressed');
          eq(f.raw(),'-'+positive,tag+' negative raw');
          eq(f.value(),whole?{num:3,den:4,whole:-2}:{num:-3,den:4},'negative value');
          eq(MaffsAnswer.fractionForm(f.raw(),whole?{whole:-2,num:3,den:4}:{num:-3,den:4},{form:whole?'mixed':'simplest'}),'correct','existing parser');
          for(const el of f.inputs) {
            el.dispatchEvent(new KeyboardEvent('keydown',{key:'-',bubbles:true,cancelable:true}));
            eq(f.raw(),positive,'physical minus toggles positive');
            el.dispatchEvent(new KeyboardEvent('keydown',{key:'-',bubbles:true,cancelable:true}));
            eq(f.raw(),'-'+positive,'physical minus toggles negative');
          }
          // MaffsKeypad dispatches input, without a physical keydown.
          type(n,'-3'); eq(f.raw(),positive,'input minus toggles');
          type(n,'-3'); eq(f.raw(),'-'+positive,'input minus toggles back');
          if(whole) { type(w,'0'); eq(f.raw(),'-0 3/4','negative zero whole'); eq(f.value(),{num:-3,den:4,whole:0},'negative zero value'); }
        } else {
          type(n,'-3'); eq(n.value,'3','unsigned input still strips minus');
        }
        type(d,'0'); eq(f.value(),null,'zero denominator rejected');
        type(d,'x12345'); eq(d.value,'123','three digits only');
        f.mark('wrong'); eq(host.querySelector('.mfi.wrong')!==null,true,'mark wrong');
        f.mark('right'); eq(host.querySelector('.mfi.right')!==null,true,'mark right');
        f.mark(''); eq(host.querySelector('.mfi.right,.mfi.wrong'),null,'mark clear');
        f.clear(); eq(f.raw(),'','clear raw'); eq(f.value(),null,'clear value'); eq(f.inputs.map(e=>e.value),whole?['','','']:['',''],'clear boxes');
        if(signed) eq(host.querySelector('button').getAttribute('aria-label'),'Make negative','clear sign');
        if(whole) {
          type(w,'2'); eq(f.raw(),'2','whole only'); eq(f.value(),{num:0,den:1,whole:2},'whole only value');
          eq(f.filled(),true,'whole only filled'); f.clear();
        }
        type(n,'3'); eq(f.raw(),'3/','partial fraction'); eq(f.value(),null,'partial invalid');
        if(w) { w.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',cancelable:true})); eq(document.activeElement===n,true,'whole Enter focuses numerator'); }
        n.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',cancelable:true})); eq(document.activeElement===d,true,'numerator Enter focuses denominator');
        let submitted=0; host.addEventListener('fraction-submit',()=>submitted++,{once:true});
        d.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',cancelable:true})); eq(submitted,1,'denominator Enter submits');
        const nr=n.getBoundingClientRect(), dr=d.getBoundingClientRect(), bar=host.querySelector('.mfi-bar').getBoundingClientRect();
        eq(nr.bottom<=bar.top && bar.bottom<=dr.top,true,'stack order');
        if(w) { const wr=w.getBoundingClientRect(); eq(wr.width,nr.width,'whole width'); eq(wr.height,nr.height,'whole height'); eq(wr.right<=nr.left,true,'whole to left'); }
        if(signed) { const sr=host.querySelector('button').getBoundingClientRect(); eq(sr.height,nr.height,'sign height'); eq(sr.width,nr.width,'sign width'); }
        eq(nr.height,innerHeight<=700?40:44,'compact height');
        eq(document.documentElement.scrollWidth<=innerWidth,true,'no horizontal scroll');
      }
      // Actual touch keypad minus -> state, then digits -> raw, on every target.
      const f=MaffsFractionInput.mount(host,{whole:true,signed:true});
      if(f.inputs.length!==3) { errors.push('keypad requires three mixed-number targets'); return errors; }
      const kp=MaffsKeypad.mount(document.getElementById('keys'),{targets:f.inputs,keys:{minus:true}});
      for(let i=0;i<3;i++) {
        f.clear(); kp.select(i);
        document.querySelector('#keys [data-act="minus"]').click();
        eq(host.querySelector('button').getAttribute('aria-pressed'),'true','keypad sign on target '+i);
        document.querySelector('#keys [data-act="in"][data-val="2"]').click();
        eq(f.inputs[i].value,'2','keypad digit on target '+i);
      }
      return errors;
    }""")


def main():
    script = SOURCE.read_text(encoding='utf-8')
    errors = []
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            for width, height in [(320,568),(360,640),(375,667),(1280,700),(1280,701)]:
                context = browser.new_context(viewport={'width':width,'height':height}, has_touch=True, is_mobile=True)
                page = context.new_page()
                page.goto(base+'/?cb=fraction-modes')
                found = check(page,script)
                errors.extend('%dx%d: %s'%(width,height,e) for e in found)
                print('%dx%d: %s'%(width,height,'PASS' if not found else found))
                context.close()
            page = browser.new_page(viewport={'width':320,'height':568},has_touch=True,is_mobile=True)
            page.goto(base+'/?cb=fraction-plants')
            for name, before, after in PLANTS:
                planted = pc.apply_plant(script,before,after,name=name)
                caught = check(page,planted)
                print('PLANT %s: %s'%(name,'CAUGHT' if caught else 'MISSED'))
                if not caught: errors.append('plant missed: '+name)
            browser.close()
    finally:
        proc.terminate(); proc.wait(timeout=10)
    for error in errors: print('FAIL: '+error)
    print('PASS: default, whole, signed, combined; five layout sizes; %d plants caught'%len(PLANTS) if not errors else 'FAILED')
    return bool(errors)


if __name__ == '__main__':
    sys.exit(main())
