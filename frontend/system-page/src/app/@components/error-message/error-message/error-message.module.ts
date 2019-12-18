import { NgModule } from '@angular/core';
import { CommonModule } from "@angular/common";
import {  ErrorMessageComponent } from './error-message.component';
import { NbAlertModule } from '@nebular/theme';


@NgModule({
  imports: [
    CommonModule,
    NbAlertModule
  ],
  declarations: [ErrorMessageComponent],
  exports: [ErrorMessageComponent],
})
export class ErrorMessageModule { }
