import { State, Action,Selector, StateContext, Store } from '@ngxs/store';
import { Login, Logout, JWTSetExpirationTimer, LoginError } from './auth.action';
import { tap } from 'rxjs/operators';
import { AuthService } from '../../@core/services/auth.service';
import { MapUtils } from '../../@core/utils/map-utils';
import { User } from '../../@core/data-type/user.type';
import { timer } from 'rxjs';
import { RouteNavigate } from '../../@core/services/router-handler.service';

export interface AuthStateModel {
   user:User;
   token:string;
   error:Object;
   timer:any;
 }
 @State<AuthStateModel>({
    name: 'Auth',
    defaults: {
      user:null,
      token:'',
      error:'',
      timer:null
    }
  })

export class AuthState {

  constructor(private authService:AuthService,private store: Store){}

  @Selector()
  public static getUser(state: AuthStateModel) {
      return state.user;
  }
  @Selector()
  public static getToken(state: AuthStateModel) {
      return state.token;
  }
  @Selector()
  public static getError(state: AuthStateModel) {
      return state.error;
  }
  @Selector()
  static isAuthenticated(state: AuthStateModel): boolean {
    return !!state.token;
  }

  @Action(Login)
   login(ctx: StateContext<AuthStateModel>,payload:Login) {
    return this.authService.login(payload.user)
      .pipe(
      tap((response)=>{
        if(response && response['token'] && response['user']){
          let t = <string> response['token'];
          let u = <User>MapUtils.deserialize(User,response['user'])
          ctx.patchState({
            user:u,
            token:t,
          });
         
        }
     }),
   );
 }

 @Action(Logout)
 logout(ctx: StateContext<AuthStateModel>,payload:Logout) {
    ctx.patchState({
      user: null,
      token:null,
    }); 
  }
  @Action(JWTSetExpirationTimer)
  SetExpirationTimer(ctx: StateContext<AuthStateModel>,payload:JWTSetExpirationTimer) {
    const state = ctx.getState()
    if(state.token){
      let time = this.authService.getTokenExpiredTime(state.token);
      console.log(time);
      if(time > 0){
        let timerSub = timer(time).subscribe(()=>{
          console.log('loooooooooog out',);
          this.store.dispatch(new RouteNavigate('/auth/logout/'));
        })
       
      }else if(time < 0){
        this.store.dispatch(new RouteNavigate('/auth/logout/'));
      }
    }else{
      this.store.dispatch(new RouteNavigate('/auth/login/'));
    }
  }

  @Action(LoginError)
  loginError(ctx: StateContext<AuthStateModel>,payload:LoginError) {
    ctx.patchState({
      error:payload.error
    }); 
  }

}