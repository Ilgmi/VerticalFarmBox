import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GreenhouseBoxDetailComponent } from './greenhouse-box-detail.component';

describe('GreenhouseBoxDetailComponent', () => {
  let component: GreenhouseBoxDetailComponent;
  let fixture: ComponentFixture<GreenhouseBoxDetailComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GreenhouseBoxDetailComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(GreenhouseBoxDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
