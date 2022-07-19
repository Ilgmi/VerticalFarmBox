import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { GreenhouseBoxRoutingModule } from './greenhouse-box-routing.module';
import { GreenhouseBoxListComponent } from './greenhouse-box-list/greenhouse-box-list.component';
import { GreenhouseBoxDetailComponent } from './greenhouse-box-detail/greenhouse-box-detail.component';
import {MatCardModule} from '@angular/material/card';
import {MatListModule} from '@angular/material/list';
import {MatButtonModule} from '@angular/material/button';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatSliderModule} from '@angular/material/slider';
import {MatInputModule} from '@angular/material/input';
import {MatButtonToggleModule} from '@angular/material/button-toggle';
import {LineChartModule, NgxChartsModule} from '@swimlane/ngx-charts';
import { SensorDataComponent } from './greenhouse-box-detail/sensor-data/sensor-data.component';
import {MatTabsModule} from '@angular/material/tabs';
import {MatSlideToggleModule} from '@angular/material/slide-toggle';


@NgModule({
  declarations: [
    GreenhouseBoxListComponent,
    GreenhouseBoxDetailComponent,
    SensorDataComponent
  ],
  imports: [
    CommonModule,
    GreenhouseBoxRoutingModule,
    MatCardModule,
    MatListModule,
    MatButtonModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatSliderModule,
    MatInputModule,
    MatButtonToggleModule,
    NgxChartsModule,
    MatTabsModule,
    MatSlideToggleModule,
    FormsModule,
  ]
})
export class GreenhouseBoxModule { }
