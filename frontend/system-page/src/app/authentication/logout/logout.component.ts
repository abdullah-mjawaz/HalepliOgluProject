import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { Store } from '@ngxs/store';
import { Logout } from '../store/auth.action';


@Component({
  selector: 'app-logout',
  templateUrl: './logout.component.html',
})
export class LogoutComponent  {
  constructor(private router:Router, private store:Store){
    this.store.dispatch(new Logout())
    router.navigate(['/auth/login'])

  }
   
}

