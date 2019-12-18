export interface ServerResponseModel<T>{
    list: Map<number,T[]>;
    page:T[];
    pageNumber:number;
    loading:boolean;
    count:number;
    errors:any;
    searchparam :ServerSearchParameters;
    newInstance:T
    detailedInstance:T
    filterParams?:FilterParameter[];
}
export interface FilterParameter{
  key:string;
  value:string;
}

export interface ServerSearchParameters{
  searchText:string;
  ordering:string;
  limit:number;
  offset:number;
  filterParams:FilterParameter[]
}

export interface IJsonMetaData<T> {
  name?: string
  clazz?: {new(): T}
}

  export class IconURL{
    id:number
    url:URL;
    icon:Icon;
    constructor(icon?,url?,id?){
      this.icon=icon;
      this.url= url;
      this.id = id;
    }
  }
  export interface Icon{
    iconName:string;
    iconStatus:string;
    iconPack:string;
}