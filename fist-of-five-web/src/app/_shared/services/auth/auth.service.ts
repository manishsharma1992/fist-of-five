import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private readonly AUTH_SERVICE_BASE_URI = "http://localhost:5000/api/users"

  httpClient = inject(HttpClient);

  constructor() { }

  registerUser(registerRequest: any): Observable<any> {
    return this.httpClient.post<any>(`${this.AUTH_SERVICE_BASE_URI}/register-user`, registerRequest);
  }
}
