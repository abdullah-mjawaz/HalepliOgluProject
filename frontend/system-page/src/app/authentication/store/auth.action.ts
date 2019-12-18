export class Login {
    static readonly type = '[Auth] Login User';
    constructor(public user :any) {}
}

export class Logout {
    static readonly type = '[Auth] Logout User';
    constructor() {}  
}

export class JWTSetExpirationTimer {
    static readonly type = '[Auth] JWT Set Expiration Timer';
    constructor() {}  
}
export class LoginError {
    static readonly type = '[Auth] Login Error';
    constructor(public error:any) {}  
}



