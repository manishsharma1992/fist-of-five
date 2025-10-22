import { CommonModule } from '@angular/common';
import { Component, inject, input, OnInit } from '@angular/core';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { timer } from 'rxjs';

@Component({
  selector: 'app-alert',
  imports: [MatSnackBarModule, CommonModule],
  templateUrl: './alert.html',
  styleUrl: './alert.scss',
  standalone: true,
})
export class Alert implements OnInit {
  
  type = input.required<string>();
  message = input.required<string>();
  duration = input<number>(3000);

  snackBar = inject(MatSnackBar);

  show!: boolean;

  constructor() {
    timer(this.duration()).subscribe(() => {
      this.show = true;
    });
  }

  ngOnInit(): void {
    console.log(this.type());
    
    this.show = true;
  }

  close() : void {
    this.show = false;
  }
}
