import { Component, inject, OnInit, signal } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ForbiddenUsernameDirective } from '../../shared/directives/forbidden-username.directive';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { RouterModule } from '@angular/router';
import { Logo } from '../../shared/components/logo/logo';
import { Waves } from '../../shared/components/waves/waves';
import { Loader } from '../../shared/services/loader';

@Component({
  selector: 'app-login',
  providers: [Loader],
  imports: [
    RouterModule,
    ReactiveFormsModule,
    ForbiddenUsernameDirective,
    MatFormFieldModule,
    MatInputModule,
    MatIconModule,
    MatButtonModule,
    Logo, 
    Waves
  ],
  templateUrl: './login.html',
  styleUrl: './login.scss',
  standalone: true
})
export class Login implements OnInit {
  

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
