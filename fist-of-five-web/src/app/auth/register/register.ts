import { Component, inject, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCard, MatCardContent, MatCardHeader, MatCardTitle, MatCardSubtitle, MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { AuthService } from '../auth-service';

import { Alert } from '../../shared/alert/alert';

@Component({
  selector: 'app-register',
  imports: [
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatIconModule,
    MatChipsModule,
    MatButtonModule,
    ReactiveFormsModule,
    Alert,
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

  registrationForm!: FormGroup;
  failureResponse!: any;

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
    this.authService.registerUser(this.registrationForm.getRawValue()).subscribe({
      next: (response: any) => {
        console.log(response);
      },
      error: (err: any) => {
        this.failureResponse = err;
        console.log(this.failureResponse)
      },
    });
  }
}
