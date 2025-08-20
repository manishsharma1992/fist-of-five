import {
  ChangeDetectionStrategy,
  Component,
  inject,
  OnInit,
  signal,
} from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { MatFormFieldModule, MatFormField, MatLabel } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatDividerModule } from '@angular/material/divider';
import { MatSelectModule } from '@angular/material/select';
import { TextInputComponent } from '../../_shared/components/input/text-input/text-input.component';
import { ForbiddenUsernameDirective } from '../../_shared/directives/forbidden-username.directive';

@Component({
  selector: 'app-login',
  imports: [
    ReactiveFormsModule,
    ForbiddenUsernameDirective,
    MatFormFieldModule,
    MatInputModule,
    MatIconModule,
    MatButtonModule
],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LoginComponent implements OnInit {
  loginForm!: FormGroup;
  formBuilder = inject(FormBuilder);
  hide = signal(true);

  ngOnInit(): void {
    this.loginForm = this.formBuilder.group({
      username: ['', [Validators.required]],
      password: ['', [Validators.required]]
    });
  }

  login(): void {
    
  }
}
