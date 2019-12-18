import 'reflect-metadata';
import { IJsonMetaData } from '../data-type/generic.type'; 

const jsonMetadataKey = "jsonProperty";

export function JsonProperty<T>(metadata?:IJsonMetaData<T>|string): any {
    if (metadata instanceof String || typeof metadata === "string"){
        return Reflect.metadata(jsonMetadataKey, {
            name: metadata,
            clazz: undefined
        });
    } else {
        let metadataObj = <IJsonMetaData<T>>metadata;
        return Reflect.metadata(jsonMetadataKey, {
            name: metadataObj ? metadataObj.name : undefined,
            clazz: metadataObj ? metadataObj.clazz : undefined
        });
    }
}


export  function logType(){
    return function (target : any, propertyKey : string) {
    var t = Reflect.getMetadata("design:type", target, propertyKey);
    console.log(`${propertyKey} type: ${t.name}`);
    }
}

export function logParamTypes
    (target : any, key : string) {
    var types = Reflect.getMetadata("design:paramtypes", target, key);
    var s = types.map(a => a.name).join();
    console.log(`${key} param types: ${s}`);
  } 

export  function IdRelatedField(){
    return function (target : any, propertyKey : string) {
    var t = Reflect.getMetadata("design:type", target, propertyKey); 
    console.log(`${propertyKey} type: ${t.name}`,target[propertyKey]);
    }
}