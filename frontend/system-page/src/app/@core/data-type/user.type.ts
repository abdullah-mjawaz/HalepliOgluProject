import { JsonProperty } from '../decorators/json-property';
import { Icon } from './generic.type';
export class User {
    public static icon: Icon = { 
        iconName:'fas fa-user',
        iconStatus:'success',
        iconPack:'font-awesome',
    };
    @JsonProperty('id')
    public id: number;
    @JsonProperty('email')
    public email: string;
    @JsonProperty('username')
    public username: string;
 
    constructor(){
        this.email=null;
        this.id=null;
        this.username=null;
    }
    public toString() : string {

        return this.username? `${this.username}`:'';
    }
    public getIcon(){
        return User.icon;
    }
}




 