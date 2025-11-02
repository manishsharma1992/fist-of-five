import { Component, inject, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { AuthService } from '../auth-service';

import { RouterModule } from '@angular/router';
import { Logo } from '../../shared/components/logo/logo';
import { Loader } from '../../shared/services/loader';
import { finalize } from 'rxjs';
import { AsyncPipe } from '@angular/common';
import { LottiePlayer } from '../../shared/components/lottie-player/lottie-player';
import { Waves } from '../../shared/components/waves/waves';
import { AlertBar } from '../../shared/components/alert-bar/alert-bar';

@Component({
  selector: 'app-register',
  providers: [Loader],
  imports: [
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatIconModule,
    MatChipsModule,
    MatButtonModule,
    ReactiveFormsModule,
    RouterModule,
    AlertBar,
    AsyncPipe,
    Logo,
    LottiePlayer,
    Waves,
  ],
  templateUrl: './register.html',
  styleUrl: './register.scss',
  standalone: true,
})
export class Register implements OnInit {
  readonly roles: string[] = [
    $localize`:@@observerRoleText:observatrice`,
    $localize`:@@estimatorRoleText:estimateur`,
  ];

  fb = inject(FormBuilder);
  authService = inject(AuthService);
  loader = inject(Loader);

  registrationForm!: FormGroup;
  failureResponse!: any;
  successResponse!: any;

  ngOnInit(): void {
    this.registrationForm = this.fb.group({
      uid: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      first_name: ['', Validators.required],
      middle_name: [],
      last_name: ['', Validators.required],
      password: ['', [Validators.required, Validators.minLength(8)]],
      role: ['', Validators.required],
    });
  }

  onRegisterSubmit() {
    if (this.registrationForm.valid) {
      this.loader.show();
      this.authService
        .registerUser(this.registrationForm.getRawValue())
        .pipe(finalize(() => this.loader.hide()))
        .subscribe({
          next: (response: any) => {
            this.successResponse = response;
            console.log(this.successResponse);
          },
          error: (err: any) => {
            this.failureResponse = err;
            if(Array.isArray(this.failureResponse?.error?.detail)) { 
              this.failureResponse.error.detail.forEach((element: any) => {
                const fieldName = element.loc?.[element.loc.length - 1];
                console.log(fieldName);
                
                const message = element.msg;
                const control = this.registrationForm.get(fieldName);
                if (control) {
                  control.setErrors({ serverError: message });
                  control.markAsTouched();
                  control.updateValueAndValidity();
                }
              });
            }
            console.log(this.failureResponse);
          },
        });
    } else {
      this.registrationForm.markAllAsTouched();
      this.registrationForm.updateValueAndValidity();
    }
  }

  get isFailureResponseTypeofArray(): boolean {
    return Array.isArray(this.failureResponse?.error?.detail);
  }
}
