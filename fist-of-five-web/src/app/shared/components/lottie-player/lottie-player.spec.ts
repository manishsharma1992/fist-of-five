import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LottiePlayer } from './lottie-player';

describe('LottiePlayer', () => {
  let component: LottiePlayer;
  let fixture: ComponentFixture<LottiePlayer>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LottiePlayer]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LottiePlayer);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
