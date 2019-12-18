import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Actions, ofActionDispatched } from '@ngxs/store';

export class RouteNavigate{
    static readonly type = '[Router] Route Navigate';
    constructor(public route:string) {}
}

@Injectable({
    providedIn: 'root'
})
export class RouteHandler {
  constructor(private router: Router, private actions$: Actions) {
    this.actions$
      .pipe(ofActionDispatched(RouteNavigate))
      .subscribe(({ route }) => this.router.navigate([route]));
  }
}