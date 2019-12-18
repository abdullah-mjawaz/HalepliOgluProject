import { Injectable } from '@angular/core';
import { HttpInterceptor } from '@angular/common/http';
import { Store } from '@ngxs/store';
import { AuthState  } from '../../authentication/store/auth.store';
@Injectable({
  providedIn: 'root'
})
export class TokenInterceptorService implements HttpInterceptor {
  
  constructor(private store:Store) { }
  intercept(req , next){
    const token = this.store.selectSnapshot(AuthState.getToken);
    const isAuthenticated = this.store.selectSnapshot(AuthState.isAuthenticated);
    if(isAuthenticated && !req.url.includes('yandex')){
          var JWT = "Bearer " + token
                        req = req.clone({
                            setHeaders: {  
                              Authorization: JWT,
                            },
                        });
          console.log('the user has been logged in with the token :',req)
          return next.handle(req);
        
      }else{
          return next.handle(req)
      }
   
  }

  
}
