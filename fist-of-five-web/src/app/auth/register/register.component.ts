import { CommonModule } from '@angular/common';
import { ChangeDetectorRef, Component, Renderer2 } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';

@Component({
  selector: 'app-register',
  imports: [ReactiveFormsModule, MatFormFieldModule, MatInputModule, CommonModule, MatCardModule],
  templateUrl: './register.component.html',
  styleUrl: './register.component.scss',
  standalone: true
})
export class RegisterComponent {
  loginForm!: FormGroup;
  isPasswordFocused = false;
  showPassword: boolean = false;

  constructor(
    private renderer: Renderer2,
    private fb: FormBuilder,
    private cdRef: ChangeDetectorRef
  ) {
    console.log("Hi from show password", this.showPassword);

    this.loginForm = this.fb.group({
      password: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]]
    });
  }

  ngOnChanges () {
  }
  ngOnInit(): void {
    this.showPassword = false; // ✅ Explicitly set again
    this.cdRef.detectChanges();

    throw new Error('Method not implemented.');
    
  }

  onPasswordFocus(focus: boolean) {
    this.isPasswordFocused = focus;
    const avatar = document.getElementById('userAvatar');
    if (avatar) {
      avatar.classList.toggle('focus', focus);
    }
  }

  handleInput() {
    // Optional: Handle input for dynamic animations
  }

  togglePassVisibility () {
    this.showPassword = !this.showPassword;

  }

  onSubmit() {
    if (this.loginForm.valid) {
      console.log('Form submitted', this.loginForm.value);
      let body =  {
        username: this.loginForm.get('email')?.value,
        password: this.loginForm.get('password')?.value
      }

      console.log("Hello for login body: ", body);
      
    }
  }
}
