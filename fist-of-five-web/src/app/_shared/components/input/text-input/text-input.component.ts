import { Component, input } from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { TranslateModule } from '@ngx-translate/core';

@Component({
  selector: 'app-text-input',
  imports: [MatFormFieldModule, MatInputModule, ReactiveFormsModule, TranslateModule],
  templateUrl: './text-input.component.html',
  styleUrl: './text-input.component.scss'
})
export class TextInputComponent {

  fieldLabel = input.required<string>();
  fieldPlaceholder = input.required<string>();
  fieldFormControl = input.required<FormControl>();
  inputType = input.required<string>();

}
