import { AbilityConstant, ConfigurationConstant, UIAbility, Want } from '@kit.AbilityKit';
import { hilog } from '@kit.PerformanceAnalysisKit';
import { window } from '@kit.ArkUI';

// 自定义一个日志的Domain ID，建议使用0x0000到0xFFFF之间的值
const DOMAIN = 0x0001;
// 自定义日志Tag
const TAG = 'LifecycleTag';

export default class EntryAbility extends UIAbility {

  // UIAbility实例创建时回调
  onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    this.context.getApplicationContext().setColorMode(ConfigurationConstant.ColorMode.COLOR_MODE_NOT_SET);
    hilog.info(DOMAIN, TAG, '%{public}s', 'Lifecycle ==> %{public}s', 'onCreate called.');
  }

  // UIAbility实例销毁时回调
  onDestroy(): void {
    hilog.info(DOMAIN, TAG, 'Lifecycle ==> %{public}s', 'onDestroy called.');
  }

  // WindowStage创建完成时回调
  onWindowStageCreate(windowStage: window.WindowStage): void {
    hilog.info(DOMAIN, TAG, 'Lifecycle ==> %{public}s', 'onWindowStageCreate called.');

    // 设置UI页面加载
    windowStage.loadContent('pages/Index', (err) => {
      if (err.code) {
        hilog.error(DOMAIN, TAG, 'Failed to load the content. Cause: %{public}s', JSON.stringify(err));
        return;
      }
      hilog.info(DOMAIN, TAG, 'Succeeded in loading the content.');
    });
  }

  // WindowStage销毁时回调
  onWindowStageDestroy(): void {
    hilog.info(DOMAIN, TAG, 'Lifecycle ==> %{public}s', 'onWindowStageDestroy called.');
  }

  // UIAbility进入前台时回调
  onForeground(): void {
    hilog.info(DOMAIN, TAG, 'Lifecycle ==> %{public}s', 'onForeground called.');
  }

  // UIAbility进入后台时回调
  onBackground(): void {
    hilog.info(DOMAIN, TAG, 'Lifecycle ==> %{public}s', 'onBackground called.');
  }
}