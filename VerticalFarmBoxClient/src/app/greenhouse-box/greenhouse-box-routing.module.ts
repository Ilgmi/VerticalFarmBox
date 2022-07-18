import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {GreenhouseBoxListComponent} from './greenhouse-box-list/greenhouse-box-list.component';
import {GreenhouseBoxDetailComponent} from './greenhouse-box-detail/greenhouse-box-detail.component';

const routes: Routes = [
  {path: '', component: GreenhouseBoxListComponent},
  {path: 'box/:id', component: GreenhouseBoxDetailComponent}
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class GreenhouseBoxRoutingModule { }
