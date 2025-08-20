import { CommonModule } from '@angular/common';
import {
  ChangeDetectorRef,
  Component,
  inject,
  OnInit,
  Renderer2,
} from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { ForbiddenUsernameDirective } from '../../_shared/directives/forbidden-username.directive';
import { MatButtonModule } from '@angular/material/button';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { AuthService } from '../../_shared/services/auth/auth.service';

@Component({
  selector: 'app-register',
  imports: [
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatCardModule,
    MatButtonModule,
    MatSlideToggleModule,
    ForbiddenUsernameDirective,
  ],
  templateUrl: './register.component.html',
  styleUrl: './register.component.scss',
  standalone: true,
})
export class RegisterComponent implements OnInit {
  registerForm!: FormGroup;
  fb = inject(FormBuilder);
  authService = inject(AuthService);

  ngOnInit(): void {
    this.registerForm = this.fb.group({
      uid: ['', [Validators.required]],
      firstName: ['', [Validators.required, Validators.minLength(3)]],
      lastName: ['', [Validators.required, Validators.minLength(3)]],
      password: ['', [Validators.required]],
      role: [''],
    });
  }

  register(): void {
    if (this.registerForm.valid) {
      const rawFormValues = this.registerForm.getRawValue();
      if (!rawFormValues['role']) {
        rawFormValues['role'] = 'Estimator';
      } else {
        rawFormValues['role'] = 'Observer';
      }

      this.authService.registerUser(rawFormValues).subscribe({
        next: (response) => {
          console.log(response);
        },
      });
    }
  }
}
