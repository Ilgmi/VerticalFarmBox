import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GreenhouseBoxListComponent } from './greenhouse-box-list.component';

describe('GreenhouseBoxListComponent', () => {
  let component: GreenhouseBoxListComponent;
  let fixture: ComponentFixture<GreenhouseBoxListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GreenhouseBoxListComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(GreenhouseBoxListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
