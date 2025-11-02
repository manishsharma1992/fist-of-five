import { Component, computed, effect, input } from '@angular/core';
import { LottiePlayer } from '../lottie-player/lottie-player';

type AlertType = 'success' | 'error' | 'info' | 'warning';
type MessageItem = string | { msg: string } | Array<{ msg: string }>;

interface AlertTheme {
  bg: string;
  text: string;
  border: string;
  lottiePath: string;
}

@Component({
  selector: 'app-alert-bar',
  imports: [LottiePlayer],
  templateUrl: './alert-bar.html',
  styleUrl: './alert-bar.scss',
})
export class AlertBar {
  message = input.required<MessageItem>();
  type = input.required<AlertType>();
  
  // Extract `.msg` from object/array, fallback to string
  messageLines = computed((): string[] => {
    const msg = this.message();

    // Case 1: string
    if (typeof msg === 'string') {
      return [msg];
    }

    // Case 2: single object { msg: "..." }
    if (msg && typeof msg === 'object' && 'msg' in msg && !Array.isArray(msg)) {
      return [(msg as { msg: string }).msg];
    }

    // Case 3: array of objects [{ msg: "..." }, ...]
    if (Array.isArray(msg)) {
      return msg
        .filter((item): item is { msg: string } => !!item && typeof item === 'object' && 'msg' in item)
        .map(item => item.msg);
    }

    // Fallback
    return [''];
  });

  private alertThemes: Record<AlertType, AlertTheme> = {
    success: {
      bg: '#E4EDE7', // Green_60
      text: '#000000',
      border: '#3a6b4d', // Success base
      lottiePath: '/images/stamp.json', // Your success animation
    },
    error: {
      bg: '#F8E2E0', // Red_70
      text: '#000000',
      border: '#c0281B',
      lottiePath: '/images/broken-file.json',
    },
    info: {
      bg: '#DDE8F0', // Blue_70
      text: '#000000',
      border: '#2a607f',
      lottiePath: '/images/info.json',
    },
    warning: {
      bg: '#F3E2D6', // Orange_70
      text: '#000000',
      border: '#a56134',
      lottiePath: '/images/warning.json',
    },
  };

  theme = computed(() => this.alertThemes[this.type()]);
}
