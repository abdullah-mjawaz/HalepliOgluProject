import { Component, ViewChild, ElementRef, OnInit } from '@angular/core';
import { Scene, WebGLRenderer, PerspectiveCamera, BoxGeometry, MeshBasicMaterial,
         Mesh, AmbientLight, DirectionalLight, PointLight, Color, TextureLoader, MeshPhongMaterial } from 'three';

import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { OrbitControls } from 'three-orbitcontrols-ts';

@Component({
  selector: 'ngx-dashboard',
  templateUrl: './dashboard.component.html',
})
export class DashboardComponent {
  @ViewChild('rendererContainer',{static:true}) canvas: ElementRef;
  title = 'threedtest';
  private renderer: WebGLRenderer;
  private camera: PerspectiveCamera;
  private loader:GLTFLoader;
  private controls:OrbitControls;
  public scene: Scene;
 
  
  //public controls: OrbitControls;
  public fieldOfView: number = 60;
  public nearClippingPane: number = 1;
  public farClippingPane: number = 1100;
  constructor(){

  }
  ngOnInit(){
    this.loader = new GLTFLoader();
    this.renderer = new WebGLRenderer();
    //create the secne
    this.scene = new Scene();
    this.scene.background = new Color(0xdddddd);
    //camera
    this.camera = new PerspectiveCamera(10, this.getAspectRatio(), 1, 1000);
    this.camera.position.z = 10;
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
   
    //this.camera = new PerspectiveCamera(40,this.getAspectRatio(),1,1100);
    //this.camera.rotation.y = 45/180*Math.PI;
    //this.camera.position.x = 800;
    //this.camera.position.y = 100;
    //this.camera.position.z = 1000;
    //control
    //this.controls = new OrbitControls(this.camera);
    let hlight = new AmbientLight (0x404040,100);
    //lights
    //this.scene.add(hlight);
    let directionalLight = new DirectionalLight(0xffffff,100);
    directionalLight.position.set(0,1,0);
    directionalLight.castShadow = true;
    //this.scene.add(directionalLight);
    let light = new PointLight(0xc0c0c0,2);
    light.position.set(0,1300,1500);
    this.scene.add(light);
    let light2 = new PointLight(0xc0c0c0,2);
    light2.position.set(1500,1000,0);
    this.scene.add(light2);
    let light3 = new PointLight(0xc0c0c0,2);
    light3.position.set(0,1000,-1500);
    this.scene.add(light3);
    let light4 = new PointLight(0xc0c0c0,2);
    light4.position.set(-1500,1300,1500);
    this.scene.add(light4);
  }
  ngAfterViewInit() {
    this.loader.load(
      '../assets/3d Models/container_low_poly/scene.gltf',
      ( gltf ) => {
          // called when the resource is loaded
          let car = gltf.scene.children[0];
          car.scale.set(0.5,0.5,0.5);
          
          this.scene.add(car);
          this.animate();
           
      },
      ( xhr ) => {
          // called while loading is progressing
          console.log( `${( xhr.loaded / xhr.total * 100 )}% loaded` );
      },
      ( error ) => {
          // called when loading has errors
          console.error( 'An error happened', error );
      },
    );
    /*this.mtlLoader.load('../assets/3d Models/truck2/texture.mtl', (materials) => {
      materials.preload()
      this.objLoader.setMaterials(materials)
      this.objLoader.load('../assets/3d Models/truck2/object.obj', (object) => {
 
        this.scene.add(object)
      })
    })*/
    
    this.renderer.setSize(this.canvas.nativeElement.clientWidth, this.canvas.nativeElement.clientHeight);
    this.canvas.nativeElement.appendChild(this.renderer.domElement);  
  }
  private getAspectRatio(): number {
    let height = this.canvas.nativeElement.clientHeight;
    if (height === 0) {
        return 0;
    }
    return this.canvas.nativeElement.clientWidth / this.canvas.nativeElement.clientHeight;
  }
 
    animate() {
      //this.camera.position.x += 0.01;
      window.requestAnimationFrame(() => this.animate()); 
      this.renderer.render(this.scene, this.camera);
    } 
}
