import { Injectable,inject, Inject } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { User } from '../data-type/user.type';
import { Observable, of } from 'rxjs';
import { catchError } from 'rxjs/operators';
import * as jwt_decode from 'jwt-decode';
import { environment } from '../../../environments/environment';
import { Store } from '@ngxs/store';
import { LoginError } from '../../authentication/store/auth.action';

export const TOKEN_NAME: string = 'jwt_token';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  constructor(private http:HttpClient, private store:Store) {
        
  }
  getToken(): string {
    return localStorage.getItem('token');
  }

  setToken(token: string): void {
    localStorage.setItem(TOKEN_NAME, token);
  }

  getTokenExpirationDate(token: string): Date {
    const decoded = jwt_decode(token);

    if (decoded.exp === undefined) 
      return null;

    const date = new Date(0); 
    date.setUTCSeconds(decoded.exp);
    return date;
  }
  
  isTokenExpired(token?: string): boolean {
    if(!token) token = this.getToken();
    if(!token) return true;

    const date = this.getTokenExpirationDate(token);
    if(date === undefined) return false;
    return !(date.valueOf() > new Date().valueOf());
  }
  getTokenExpiredTime(token?: string): number {
    if(!token) token = this.getToken();
    if(!token) return 0;

    const date = this.getTokenExpirationDate(token);
    if(date === undefined) return 0;
    let now = new Date();
    let subs = Math.abs(date.valueOf() - now.valueOf());
    return subs;
  }

  login(user:User){ 
      return  this.http.post(environment.OBTAIN_TOKEN_URL, user)
      .pipe(
        catchError(this.handleError<User>(LoginError, null))
      );
  }

  private handleError<T> (storeAction , result?: T) {
    return (error: HttpErrorResponse): Observable<T> => {
      
      // TODO: send the error to remote logging infrastructure
      // log to console instead
      console.log('this is the error',error,storeAction); 
      this.store.dispatch(new storeAction(error['error']));
      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }

}
