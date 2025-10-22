import { Directive, ElementRef, HostListener } from '@angular/core';
import { NgControl } from '@angular/forms';

@Directive({
  selector: '[appCapitalizeWords]'
})
export class CapitalizeWordsDirective {

  constructor(private el: ElementRef, private control: NgControl) {}

  @HostListener('input', ['$event'])
  onInput(event: Event) {
    const input = event.target as HTMLInputElement;
    const transformed = this.capitalizeWords(input.value);

    // only update if changed (avoid cursor jump issues)
    if (input.value !== transformed) {
      input.value = transformed;

      // keep Angular forms in sync
      if (this.control && this.control.control) {
        this.control.control.setValue(transformed, {
          emitEvent: false, // avoid double event loops
          emitModelToViewChange: false,
          emitViewToModelChange: true,
        });
      }
    }
  }

  private capitalizeWords(value: string): string {
    return value
      .split(' ')
      .map(word =>
        word.length > 0
          ? word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
          : ''
      )
      .join(' ');
  }

}
