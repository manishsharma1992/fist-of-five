import { AfterViewInit, Component, effect, ElementRef, input, OnDestroy, viewChild } from '@angular/core';

@Component({
  selector: 'app-lottie-player',
  imports: [],
  templateUrl: './lottie-player.html',
  styleUrl: './lottie-player.scss',
  standalone: true,
})
export class LottiePlayer implements AfterViewInit, OnDestroy {

  path = input.required<string>();
  autoplay = input(true);
  loop = input(true);
  speed = input(1);
  renderer = input<'svg' | 'canvas' | 'html'>('svg');

  private container = viewChild.required<ElementRef<HTMLDivElement>>('lottie.container');
  private anim: any = null;

  constructor() {
    // React to any input change
    effect(() => {
      this.path(); // Trigger on any input change
      this.destroyAnimation();
      this.load();
    });
  }

  ngAfterViewInit(): void {
    this.load();
  }

  ngOnDestroy(): void {
    this.anim?.destroy();
  }

  private async load(): Promise<void> {
    if (!this.path()) return;

    try {
      // Dynamic import = ESM safe
      const lottie = await import('lottie-web');

      this.anim = lottie.default.loadAnimation({
        container: this.container().nativeElement,
        renderer: this.renderer(),
        loop: this.loop(),
        autoplay: this.autoplay(),
        path: this.path(),
        rendererSettings: {
          progressiveLoad: true,
          preserveAspectRatio: 'xMidYMid meet',
        },
      });

      this.anim.setSpeed(this.speed());
    } catch (err) {
      console.error('Failed to load lottie-web:', err);
    }
  }

  private destroyAnimation(): void {
    if (this.anim) {
      this.anim.destroy();
      this.anim = null;
    }
  }

}
