import { Injectable } from '@angular/core';
import { CanActivate, Router, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { Observable } from 'rxjs';
import { Select, Store } from '@ngxs/store';
import { AuthState  } from '../store/auth.store';
import { AuthService } from '../../@core/services/auth.service'


@Injectable()
export class AuthGuard implements CanActivate {
  @Select(AuthState.isAuthenticated) isAuth$: Observable<boolean>;
  constructor(private router: Router,private store :Store,private authService:AuthService) { }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean  {
    const token = this.store.selectSnapshot(AuthState.getToken);
    const isAuthenticated = this.store.selectSnapshot(AuthState.isAuthenticated);
    if(isAuthenticated && !this.authService.isTokenExpired(token)){
      return true;
    }else{
      return false;
    }

    // console.log(token,isAuthenticated)
    // console.log(this.authService.getTokenExpirationDate(token))
    // console.log(this.authService.isTokenExpired(token))
    
  }   

}