
import { FormControl, FormGroup,  } from '@angular/forms';
import { parsePhoneNumberFromString } from 'libphonenumber-js';
export class ValidationService {
    static getValidatorErrorMessage(validatorName: string, validatorValue?: any) {
        let config = {
            'required': 'required',
            'serverError': `${validatorValue}`,
            'invalidCreditCard': 'Is invalid credit card number',
            'invalidEmailAddress': 'Invalid email address',
            'invalidPassword': 'Invalid password. Password must be at least 6 characters long, and contain a number.',
            'minlength': `Minimum length ${validatorValue.requiredLength}`,
            'invalidInteger':'Is invalid  number',
            'invalidName':'invalid  Name',
            'notSame':'password must match',
            'invalidPhoneNumber':'invalid phone number',
            'invalidPositiveNumber':'invalid positive number',
        };

        return config[validatorName];
    }

    static creditCardValidator(control:FormControl) {
        // Visa, MasterCard, American Express, Diners Club, Discover, JCB
        if (control.value.match(/^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})$/)) {
            return null;
        } else {
            return { 'invalidCreditCard': true };
        }
    }
   
    static nameValidator(control:FormControl) {
        
        //  compliant regex
        if (control.value.match(/^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$/)) {
            return null;
        } else {
            return { 'invalidName': true };
        }
    }
    static emailValidator(control:FormControl) {
        // compliant regex
        if (control.value.match(/[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?/)) {
            return null;
        } else {
            return { 'invalidEmailAddress': true };
        }
    }

    static passwordValidator(control:FormControl) {
        // {6,100}           - Assert password is between 6 and 100 characters
        // (?=.*[0-9])       - Assert a string has at least one number
        if (control.value.match(/^(?=.*[0-9])[a-zA-Z0-9!@#$%^&*]{6,100}$/)) {
            return null;
        } else {
            return { 'invalidPassword': true };
        }
    }
    
    static positiveNumberValidator(control:FormControl) { 
        if (Math.sign(parseFloat( control.value))>0){
            return null;
        } else {
            return { 'invalidPositiveNumber': true };
        }
    }
    static IntegerValidator(control:FormControl) {
        // 
        // (*[0-9])       - Assert a string has at least one number
   
        if (control.value.match(/^[0-9]*$/)) {
            return null;
        } else {
            return { 'invalidInteger': true };
        }
    }
    static checkPasswords(group: FormGroup) { // here we have the 'passwords' group
        let pass = group.controls.password1.value;
        let confirmPass = group.controls.password2.value;

        return pass === confirmPass ? null : { notSame: true }
  }
  static phoneNumberValidator(control:FormControl) {
    // compliant regex
    const phoneNumber = parsePhoneNumberFromString(control.value)


    if ( phoneNumber &&  phoneNumber.isValid()) {
        return null;
    } else {
        return { 'invalidPhoneNumber': true };
    }
}


}
