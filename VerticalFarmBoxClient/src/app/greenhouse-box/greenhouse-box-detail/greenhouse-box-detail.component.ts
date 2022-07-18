import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, ParamMap} from '@angular/router';
import {GreenhouseBoxApiService} from '../greenhouse-box-api.service';
import {BehaviorSubject, Observable, switchMap} from 'rxjs';
import {GreenhouseBox} from '../domain/greenhouse-box';
import {GreenhouseBoxListComponent} from '../greenhouse-box-list/greenhouse-box-list.component';
import {AbstractControl, FormBuilder, FormGroup, ValidationErrors, ValidatorFn, Validators} from '@angular/forms';
import {MatSnackBar} from '@angular/material/snack-bar';


@Component({
  selector: 'app-greenhouse-box-detail',
  templateUrl: './greenhouse-box-detail.component.html',
  styleUrls: ['./greenhouse-box-detail.component.css']
})
export class GreenhouseBoxDetailComponent implements OnInit {

  public isLoading$ = new BehaviorSubject(false);
  public box!: GreenhouseBox;
  public currentBox$: Observable<GreenhouseBox>;



  public conditionForm!: FormGroup;

  constructor(private route: ActivatedRoute, private boxService: GreenhouseBoxApiService,
              private fb: FormBuilder, private _snackBar: MatSnackBar) {
    this.currentBox$ = this.boxService.currentSelectedBox.asObservable();

    this.currentBox$.subscribe(x => {
      this.box = x;


      this.boxService.loadSensorData(this.box);

      const minMaxValidator: ValidatorFn = (fg: AbstractControl) => {
        const min = fg.get('min_val');
        const max = fg.get('max_val');
        return min?.value <= max?.value ? null : {range: true};
      }

      this.conditionForm = this.fb.group({
        'temperature_condition': this.fb.group({
          'min_val': this.fb.control(this.box.temperature_condition.min_val,
            [Validators.required, Validators.min(0), Validators.max(60)]),
          'max_val': this.fb.control(this.box.temperature_condition.max_val,
            [Validators.required, Validators.min(0), Validators.max(60)]),
        }, {validators: [minMaxValidator]}),
        'humidity_condition': this.fb.group({
          'min_val': this.fb.control(this.box.humidity_condition.min_val,
            [Validators.required, Validators.min(0), Validators.max(100)]),
          'max_val': this.fb.control(this.box.humidity_condition.max_val,
            [Validators.required, Validators.min(0), Validators.max(100)]),
        }, {validators: [minMaxValidator]})
      })
      this.isLoading$.next(false);
    });


  }

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id')!;
    this.isLoading$.next(true);
    this.boxService.getBox(id);
  }

  updateConditions() {
    const conditions = this.conditionForm.value;
    this.boxService.updateConditions(this.box, conditions).subscribe(
      {
        next: () => this._snackBar.open('Conditions Saved', 'Ok'),
        error: () => this._snackBar.open('Conditions Saved Failed', 'Ok')
      });
  }

  toggleRoof() {
    this.boxService.toggleRoof(this.box).subscribe({
      next: () => this._snackBar.open('Toggled', 'Ok'),
      error: () => this._snackBar.open('Toggled Failed', 'Ok')
    });
  }

  waterPlant() {
    this.boxService.waterPlant(this.box).subscribe({
      next: () => this._snackBar.open('Watering Plant', 'Ok'),
      error: () => this._snackBar.open('Watering Plant Failed', 'Ok')
    });
  }

}
