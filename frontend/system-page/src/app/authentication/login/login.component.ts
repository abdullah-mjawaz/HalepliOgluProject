import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { FormBuilder, Validators, FormGroup, FormControl  } from '@angular/forms';
//rxjs
import { Observable, Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
//store
import { Store, Select, Actions, ofActionErrored, ofActionSuccessful } from '@ngxs/store';
import { Login } from '../store/auth.action';
import { AuthState  } from '../store/auth.store';
import { ValidationService } from '../../@core/services/validation.service';
//mebular
import { NbToastrService, NbGlobalPosition, NbComponentStatus } from '@nebular/theme';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
})
export class LoginComponent implements OnInit{
  @Select(AuthState.getError) error$: Observable<Object>;  
  private unsubscribe$ =new Subject<void>();
  private loginForm:FormGroup;
  user={email:'abdullah.mjawaz@gmail.com',password:'a123456'};
  constructor(private formBuilder: FormBuilder,
              private actions: Actions,
              private router:Router,
              private store:Store,
              private toastrService: NbToastrService){
    this.loginForm = this.formBuilder.group({
      email:['', {validators: [Validators.required,ValidationService.emailValidator], updateOn: "blur"}],
      password: ['', {validators: [Validators.required,ValidationService.passwordValidator], updateOn: "blur"}],

    })
  } 
  ngOnInit(){
    let position = <NbGlobalPosition>'bottom-right';
    let status = <NbComponentStatus> 'danger';
    this.actions.pipe(ofActionSuccessful(Login)).subscribe(() => {
      this.router.navigate(['/pages/dashboard']);
    });
    this.error$.pipe(takeUntil(this.unsubscribe$))
    .subscribe((error)=>{
      if(error['non_field_errors']){
        this.toastrService.show(error['non_field_errors'],
        'Server Error',
        { position,status});
      }
    });
  }
  get email(){
    return this.loginForm.controls['email'] as FormControl
  }
  get password(){
    return this.loginForm.controls['password'] as FormControl
  }
 
  LogUserData(){
    if(this.loginForm.valid){
      this.store.dispatch(new Login(this.loginForm.value));
    }
  }
  ngOnDestroy(){ 
    this.unsubscribe$.next();
    this.unsubscribe$.complete();  
  }

}