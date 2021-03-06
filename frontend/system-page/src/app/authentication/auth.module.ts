import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule,ReactiveFormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

import { NgxAuthRoutingModule } from './auth-routing.module';
import { NbAuthModule } from '@nebular/auth';
import {NgxsModule} from '@ngxs/store'; 
import { AuthState } from './store/auth.store';
 
import { 
  NbAlertModule,
  NbButtonModule,
  NbCheckboxModule,
  NbInputModule
} from '@nebular/theme';

import { LoginComponent, } from './login/login.component'; 
import { LogoutComponent } from './logout/logout.component'
@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    RouterModule,
    NbAlertModule,
    NbInputModule,
    NbButtonModule,
    NbCheckboxModule,
    NgxAuthRoutingModule,
    NgxsModule.forFeature([AuthState]),
    NbAuthModule,
  ],
  declarations: [
    // ... here goes our new components
    LoginComponent,
    LogoutComponent
  ],
 
})
export class AuthModule {
}