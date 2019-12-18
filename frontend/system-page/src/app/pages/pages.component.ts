import { Component } from '@angular/core';

import { MENU_ITEMS } from './pages-menu';
import { JWTSetExpirationTimer } from '../authentication/store/auth.action';
import { Store } from '@ngxs/store';
@Component({
  selector: 'ngx-pages',
  styleUrls: ['pages.component.scss'],
  template: `
    <ngx-one-column-layout>
      <nb-menu [items]="menu"></nb-menu>
      <router-outlet></router-outlet>
    </ngx-one-column-layout>
  `,
})
export class PagesComponent {
  constructor(private store:Store){
    this.store.dispatch(new JWTSetExpirationTimer());
  }
  menu = MENU_ITEMS;
}
