import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private readonly BASE_URL = 'http://localhost:8000/api/v1/auth';
  private readonly http = inject(HttpClient);

  registerUser(registerFormValues: any): Observable<any> {
    return this.http.post<any>(`${this.BASE_URL}/register`, registerFormValues);
  }
}
