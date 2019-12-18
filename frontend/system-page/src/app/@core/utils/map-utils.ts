
import { IJsonMetaData } from '../data-type/generic.type'; 
const jsonMetadataKey = "jsonProperty";
export class MapUtils {
    constructor(){}
	static isPrimitive(obj) {
        switch (typeof obj) {
            case "string":
            case "number":
            case "boolean":
                return true;
        }
        return !!(obj instanceof String || obj === String ||
        obj instanceof Number || obj === Number ||
        obj instanceof Boolean || obj === Boolean);
    }
	
	static getClazz(target: any, propertyKey: string): any {
		return Reflect.getMetadata("design:type", target, propertyKey)
    }
    static isArray(object) {
        if (object === Array) {
            return true;
        } else if (typeof Array.isArray === "function") {
            return Array.isArray(object);
        }
        else {
            return !!(object instanceof Array);
        }
    }
	
	static getJsonProperty<T>(target: any, propertyKey: string):  IJsonMetaData<T> {
        return Reflect.getMetadata(jsonMetadataKey, target, propertyKey);
    }

	static deserialize<T>(clazz:{new(): T}, jsonObject) {
        if ((clazz === undefined) || (jsonObject === undefined)) return undefined;
        if (MapUtils.isArray(jsonObject) && jsonObject.length==0) return [];
        let obj = new clazz();
        Object.keys(obj).forEach((key) => {
            let propertyMetadataFn:(IJsonMetaData) => any = (propertyMetadata)=> {
                let propertyName = propertyMetadata.name || key;
                let innerJson = undefined;
                innerJson = jsonObject ? jsonObject[propertyName] : null;
                if(innerJson && innerJson==[]){
                    return [];
                }
                let clazz = MapUtils.getClazz(obj, key); 
                if (MapUtils.isArray(clazz)) { 
                    let metadata = MapUtils.getJsonProperty(obj, key);
                    if (metadata.clazz || MapUtils.isPrimitive(clazz)) { 
                        if (innerJson && MapUtils.isArray(innerJson) && innerJson.length>0) {
                            if(typeof innerJson[0] === 'number'){
                                innerJson = innerJson.map(item=>{let x ={id:item}; return x})
                            }
                            return innerJson.map(
                                (item)=> MapUtils.deserialize(metadata.clazz, item)
                            );
                        }else {
                            return null;
                        }
                    } else {
                        return innerJson;
                    }
                } else if(clazz && !MapUtils.isPrimitive(clazz) && typeof innerJson === 'number'){
                    innerJson = {id:innerJson};
                    return MapUtils.deserialize(clazz, innerJson);
                }else if (!MapUtils.isPrimitive(clazz)){
                    return MapUtils.deserialize(clazz, innerJson);
                } else {
                    return jsonObject ? jsonObject[propertyName] : undefined;
                }


            };

            let propertyMetadata = MapUtils.getJsonProperty(obj, key);
            if (propertyMetadata) {
                obj[key] = propertyMetadataFn(propertyMetadata);
            } else {
                if (jsonObject && jsonObject[key] !== undefined) {
                    obj[key] = jsonObject[key];
                }
            }
        });
        return obj;
    }
}