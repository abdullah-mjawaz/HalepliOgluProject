
import { Component, Input,OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { ValidationService } from '../../../@core/services/validation.service';

@Component({
  selector: 'error-message',
  templateUrl: './error-message.component.html',
  styleUrls: ['./error-message.component.scss']
  
})
export class ErrorMessageComponent implements OnInit {
  @Input() control: FormControl;
  @Input() form: FormGroup;
  constructor() { }

  ngOnInit() {
  }
  get controlErrorMessage() {
  
    for (let propertyName in this.control.errors) {
      if (this.control.errors.hasOwnProperty(propertyName) && this.control.touched) {
         return ValidationService.getValidatorErrorMessage(propertyName, this.control.errors[propertyName]);
      }
    }
    
  
    return null;
  }
  

}
