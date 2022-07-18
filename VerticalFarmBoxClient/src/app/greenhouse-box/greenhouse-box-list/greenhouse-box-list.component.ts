import { Component, OnInit } from '@angular/core';
import {GreenhouseBoxApiService} from '../greenhouse-box-api.service';
import {Observable} from 'rxjs';
import {GreenhouseBox} from '../domain/greenhouse-box';

@Component({
  selector: 'app-greenhouse-box-list',
  templateUrl: './greenhouse-box-list.component.html',
  styleUrls: ['./greenhouse-box-list.component.css']
})
export class GreenhouseBoxListComponent implements OnInit {


  public greenhouseBoxes$: Observable<GreenhouseBox[]>;

  constructor(private boxService: GreenhouseBoxApiService) {
    this.greenhouseBoxes$ = this.boxService.greenhouseBoxes.asObservable();
  }

  ngOnInit(): void {
    this.boxService.loadBoxes();
  }

}
