import { Directive } from '@angular/core';
import { AbstractControl, NG_VALIDATORS, ValidationErrors, Validator } from '@angular/forms';

@Directive({
  selector: '[appForbiddenUsername]',
  providers: [{provide: NG_VALIDATORS, useExisting: ForbiddenUsernameDirective, multi: true}],
})
export class ForbiddenUsernameDirective implements Validator {

  private static readonly USERNAME_REGEX = /^[a-z]\d{5}$/;

  constructor() { }
  validate(control: AbstractControl): ValidationErrors | null {
    const value = control.value as string | null | undefined;
    if(value == null || value === '') return null;

    const ok = ForbiddenUsernameDirective.USERNAME_REGEX.test(value);

    return ok ? null : {
      usernameFormat: {
        requiredPattern: '^[a-z]\\d{5}$',
        actualValue: value,
      }
    };
  }
  registerOnValidatorChange?(fn: () => void): void {
    
  }

}
