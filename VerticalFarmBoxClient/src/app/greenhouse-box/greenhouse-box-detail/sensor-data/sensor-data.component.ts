import { Component, OnInit } from '@angular/core';
import {BehaviorSubject, Observable} from 'rxjs';
import {GreenhouseBoxApiService} from '../../greenhouse-box-api.service';


interface ChartData {
  name:string
  series: {name: Date, value: any}[]
}

@Component({
  selector: 'app-sensor-data',
  templateUrl: './sensor-data.component.html',
  styleUrls: ['./sensor-data.component.css']
})
export class SensorDataComponent implements OnInit {

  public isLoading$ = new BehaviorSubject(false);
  public sensorData$: Observable<any>;


  public multi: ChartData[] = []
  public view: [number, number] = [700, 300];

  public legend: boolean = true;
  public showLabels: boolean = true;
  public animations: boolean = true;
  public xAxis: boolean = true;
  public yAxis: boolean = true;
  public showYAxisLabel: boolean = true;
  public showXAxisLabel: boolean = true;
  public xAxisLabel: string = 'Time';
  public yAxisLabel: string = 'Values';
  public timeline: boolean = true;


  colorScheme = {
    domain: ['#5AA454', '#E44D25', '#CFC0BB', '#7aa3e5', '#a8385d', '#aae3f5']
  };

  constructor(private boxService: GreenhouseBoxApiService) {
    this.isLoading$.next(true);
    this.sensorData$ = this.boxService.currentSelectedBoxSensorData.asObservable();
    this.sensorData$.subscribe(x => {

      const mappedData: ChartData[] = [];
      (x as ChartData[]).forEach(chart => {
        const d: any[] = [];
        chart.series.forEach(value => {
          d.push({name: new Date(value.name), value: value.value});
        });
        mappedData.push({
          name: chart.name,
          series: d
        })
      });
      this.multi = mappedData;
      this.isLoading$.next(false);
    });
  }

  ngOnInit(): void {
  }

  onSelect(data: any): void {
    console.log('Item clicked', JSON.parse(JSON.stringify(data)));
  }

  onActivate(data: any): void {
    console.log('Activate', JSON.parse(JSON.stringify(data)));
  }

  onDeactivate(data: any): void {
    console.log('Deactivate', JSON.parse(JSON.stringify(data)));
  }

}


const data = [
  {
    "name": "Germany",
    "series": [
      {
        "name": "2010",
        "value": 7300000
      },
      {
        "name": "2011",
        "value": 8940000
      }
    ]
  },

  {
    "name": "USA",
    "series": [
      {
        "name": "2010",
        "value": 7870000
      },
      {
        "name": "2011",
        "value": 8270000
      }
    ]
  }
];
