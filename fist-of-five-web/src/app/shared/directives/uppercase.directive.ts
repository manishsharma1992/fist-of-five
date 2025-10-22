import { Directive, ElementRef, HostListener, Optional } from '@angular/core';
import { NgControl } from '@angular/forms';

@Directive({
  selector: '[appUppercase]'
})
export class UppercaseDirective {

  private composing = false;

  constructor(
    private el: ElementRef<HTMLInputElement | HTMLTextAreaElement>,
    @Optional() private ngControl?: NgControl
  ) {}

  @HostListener('compositionstart')
  onCompositionStart() {
    this.composing = true; // IME (e.g., Hindi/Chinese) – don't interfere
  }

  @HostListener('compositionend')
  onCompositionEnd() {
    this.composing = false;
    this.transform(); // apply once composition finishes
  }

  @HostListener('input')
  onInput() {
    if (!this.composing) this.transform();
  }

  @HostListener('paste', ['$event'])
  onPaste(e: ClipboardEvent) {
    // Let paste happen, then transform in the next microtask
    setTimeout(() => this.transform());
  }

  private transform() {
    const el = this.el.nativeElement;
    const original = el.value;
    const upper = original.toUpperCase();

    if (original !== upper) {
      const start = (el as HTMLInputElement).selectionStart ?? upper.length;
      const end = (el as HTMLInputElement).selectionEnd ?? upper.length;

      el.value = upper;

      // keep cursor/selection stable
      try {
        (el as HTMLInputElement).setSelectionRange(start, end);
      } catch {}

      // keep Angular forms in sync (no extra change loops)
      this.ngControl?.control?.setValue(upper, {
        emitEvent: false,
        emitModelToViewChange: false,
        emitViewToModelChange: true,
      });
    }
  }
}
