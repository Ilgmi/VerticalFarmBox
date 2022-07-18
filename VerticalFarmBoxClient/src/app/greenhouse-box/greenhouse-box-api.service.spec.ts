import { TestBed } from '@angular/core/testing';

import { GreenhouseBoxApiService } from './greenhouse-box-api.service';

describe('GreenhouseBoxApiService', () => {
  let service: GreenhouseBoxApiService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(GreenhouseBoxApiService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
