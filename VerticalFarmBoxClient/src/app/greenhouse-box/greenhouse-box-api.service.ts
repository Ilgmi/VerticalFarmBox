import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {GreenhouseBox} from './domain/greenhouse-box';
import {BehaviorSubject, firstValueFrom, Observable, Subject} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class GreenhouseBoxApiService {


  public greenhouseBoxes: BehaviorSubject<GreenhouseBox[]> = new BehaviorSubject<GreenhouseBox[]>([])
  public currentSelectedBox: Subject<GreenhouseBox> = new Subject<GreenhouseBox>();

  public currentSelectedBoxSensorData = new Subject();

  constructor(private httpClient: HttpClient) {
  }


  public loadBoxes() {
    this.httpClient.get<GetBoxesResult>('/api/boxes/?skip=0&limit=10').subscribe(x => this.greenhouseBoxes.next(x.boxes));
  }

  public loadBox(building: string, room: string, name: string){
    this.httpClient.get<GreenhouseBox>(`api/buildings/${building}/rooms/${room}/boxes/${name}`).subscribe(x => this.currentSelectedBox.next(x));
  }

  public getBox(name: string) {
    const box = this.greenhouseBoxes.getValue().find(x => x.name === name);

    if(box){
      this.currentSelectedBox.next(box);
    }else{
     this.loadBox('U38.1', '38.01', name)
    }
  }

  public loadSensorData(box: GreenhouseBox){
    this.httpClient.get<GreenhouseBox>(`api/buildings/${box.building}/rooms/${box.room}/boxes/${box.name}/sensors-data`).subscribe(x => {
      this.currentSelectedBoxSensorData.next(x);
    })
  }

  public rotateRoof(box: GreenhouseBox, directoin: boolean, steps: number) {
    return this.httpClient.post(`api/buildings/${box.building}/rooms/${box.room}/boxes/${box.name}/move-roof`, {
      direction: directoin,
      steps: steps
    });
  }

  updateConditions(box: GreenhouseBox, conditions: any): Observable<any> {
    return this.httpClient.put(`api/buildings/${box.building}/rooms/${box.room}/boxes/${box.name}`, conditions);
  }

  toggleRoof(box: GreenhouseBox) {
    return this.httpClient.post(`api/buildings/${box.building}/rooms/${box.room}/boxes/${box.name}/toggle-roof`, {});
  }

  public waterPlant(box: GreenhouseBox) {
    return this.httpClient.post(`api/buildings/${box.building}/rooms/${box.room}/boxes/${box.name}/water-plant`, {});
  }
}

interface GetBoxesResult {
  count: number
  boxes: GreenhouseBox[]
}
