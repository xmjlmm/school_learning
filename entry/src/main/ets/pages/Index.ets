/*
 * Copyright (c) 2024 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import { BusinessError } from '@kit.BasicServicesKit';
import { fileIo, fileUri } from '@kit.CoreFileKit';
import { image } from '@kit.ImageKit';
import { resourceManager } from '@kit.LocalizationKit';
import { hilog } from '@kit.PerformanceAnalysisKit';
import CommonConstants from '../common/CommonConstants'

const TAG = 'IMAGE_COMPRESSION';

class CompressedImageInfo {
  imageUri: string = "";
  imageByteLength: number = 0;
}

async function compressedImage(sourcePixelMap: image.PixelMap,
  maxCompressedImageSize: number): Promise<CompressedImageInfo> {
  const imagePackerApi = image.createImagePacker();
  const IMAGE_QUALITY = 0;
  const packOpts: image.PackingOption = { format: "image/jpeg", quality: IMAGE_QUALITY };
  let compressedImageData: ArrayBuffer = await imagePackerApi.packToData(sourcePixelMap, packOpts)
    .catch((error: BusinessError) => {
      hilog.error(0x0000, TAG, `releaseVideo catch error, code: ${error.code}, message: ${error.message}`);
      return new ArrayBuffer(0);
    });
  const maxCompressedImageByte = maxCompressedImageSize * CommonConstants.BYTE_CONVERSION;
  if (maxCompressedImageByte > compressedImageData.byteLength) {
    compressedImageData =
      await packingImage(compressedImageData, sourcePixelMap, IMAGE_QUALITY, maxCompressedImageByte);
  } else {
    let imageScale = 1;
    const REDUCE_SCALE = CommonConstants.REDUCE_SCALE;
    while (compressedImageData.byteLength > maxCompressedImageByte) {
      if (imageScale > 0) {
        imageScale = imageScale - REDUCE_SCALE;
        await sourcePixelMap.scale(imageScale, imageScale);
        compressedImageData = await packing(sourcePixelMap, IMAGE_QUALITY);
      } else {
        break;
      }
    }
  }
  const compressedImageInfo: CompressedImageInfo = await saveImage(compressedImageData);
  return compressedImageInfo;
}

async function packing(sourcePixelMap: image.PixelMap, imageQuality: number): Promise<ArrayBuffer> {
  const imagePackerApi = image.createImagePacker();
  const packOpts: image.PackingOption = { format: "image/jpeg", quality: imageQuality };
  const data: ArrayBuffer = await imagePackerApi.packToData(sourcePixelMap, packOpts).catch((error: BusinessError) => {
    hilog.error(0x0000, TAG, `releaseVideo catch error, code: ${error.code}, message: ${error.message}`);
    return new ArrayBuffer(0);
  });
  return data;
}

async function packingImage(compressedImageData: ArrayBuffer, sourcePixelMap: image.PixelMap,
  imageQuality: number, maxCompressedImageByte: number): Promise<ArrayBuffer> {
  const packingArray: number[] = [];
  const DICHOTOMY_ACCURACY = CommonConstants.DICHOTOMY_ACCURACY;
  for (let i = 0; i <= CommonConstants.PICTURE_QUALITY_MAX; i += DICHOTOMY_ACCURACY) {
    packingArray.push(i);
  }
  let left = 0;
  let right = packingArray.length - 1;
  while (left <= right) {
    const mid = Math.floor((left + right) / 2);
    imageQuality = packingArray[mid];
    compressedImageData = await packing(sourcePixelMap, imageQuality);
    if (compressedImageData.byteLength <= maxCompressedImageByte) {
      left = mid + 1;
      if (mid === packingArray.length - 1) {
        break;
      }
      compressedImageData = await packing(sourcePixelMap, packingArray[mid + 1]);
      if (compressedImageData.byteLength > maxCompressedImageByte) {
        compressedImageData = await packing(sourcePixelMap, packingArray[mid]);
        break;
      }
    } else {
      right = mid - 1;
    }
  }
  return compressedImageData;
}

const uiContext: UIContext | undefined = AppStorage.get('uiContext');

async function saveImage(compressedImageData: ArrayBuffer): Promise<CompressedImageInfo> {
  const context: Context = uiContext!.getHostContext()!;
  const compressedImageUri: string = context.filesDir + '/' + 'afterCompression.png';
  try {
    const res = fileIo.accessSync(compressedImageUri);
    if (res) {
      fileIo.unlinkSync(compressedImageUri);
    }
    const file: fileIo.File = fileIo.openSync(compressedImageUri, fileIo.OpenMode.READ_WRITE | fileIo.OpenMode.CREATE);
    fileIo.writeSync(file.fd, compressedImageData);
    fileIo.closeSync(file);
  } catch (err) {
    hilog.error(0x0000, TAG, JSON.stringify(err));
  }
  let compressedImageInfo: CompressedImageInfo = new CompressedImageInfo();
  compressedImageInfo.imageUri = compressedImageUri;
  compressedImageInfo.imageByteLength = compressedImageData.byteLength;
  return compressedImageInfo;
}

@Entry
@Component
struct Index {
  @State compressedImageSrc: string | Resource = '';
  @State beforeCompressionSize: string = '';
  @State afterCompressionSize: string = '';
  private sourceImageByteLength: number = 0;
  private compressedByteLength: number = 0;
  private maxCompressedImageSize: number = 0;
  private context: Context = this.getUIContext().getHostContext()!;

  aboutToAppear(): void {
    const context: Context = this.getUIContext().getHostContext()!;
    const resourceMgr: resourceManager.ResourceManager = context.resourceManager;
    resourceMgr.getRawFileContent('compression.jpeg').then((fileData: Uint8Array) => {
      const buffer = fileData.buffer.slice(0);
      this.sourceImageByteLength = buffer.byteLength;
      this.beforeCompressionSize = (this.sourceImageByteLength / CommonConstants.BYTE_CONVERSION).toFixed(1);
    }).catch((err: BusinessError) => {
      hilog.error(0x0000, TAG, JSON.stringify(err));
    });
  }

  imageCompression(): void {
    const resourceMgr: resourceManager.ResourceManager = this.context.resourceManager;
    resourceMgr.getRawFileContent('compression.jpeg').then((fileData: Uint8Array) => {
      const buffer = fileData.buffer.slice(0);
      const imageSource: image.ImageSource = image.createImageSource(buffer);
      const decodingOptions: image.DecodingOptions = {
        editable: true,
        desiredPixelFormat: 3,
      }
      imageSource.createPixelMap(decodingOptions).then((originalPixelMap: image.PixelMap) => {
        compressedImage(originalPixelMap, this.maxCompressedImageSize).then((showImage: CompressedImageInfo) => {
          this.compressedImageSrc = fileUri.getUriFromPath(showImage.imageUri);
          this.compressedByteLength = showImage.imageByteLength;
          this.afterCompressionSize = (this.compressedByteLength / CommonConstants.BYTE_CONVERSION).toFixed(1);
        })
      }).catch((err: BusinessError) => {
        hilog.error(0x0000, TAG, JSON.stringify(err));
      });
    }).catch((err: BusinessError) => {
      hilog.error(0x0000, TAG, JSON.stringify(err));
    });
  }

  build() {
    Column({ space: CommonConstants.SPACE_TEN }) {
      Row({ space: CommonConstants.SPACE_TEN }) {
        Text($r('app.string.max_compression_image_size')).fontSize($r('app.float.font_size_16'))
        TextInput()
          .type(InputType.Number)
          .fontSize($r('app.float.font_size_16'))
          .width($r('app.string.text_input_width'))
          .onChange((value: string) => {
            this.maxCompressedImageSize = Number(value);
          })
      }

      Button($r('app.string.image_compression')).onClick(() => {
        if (this.maxCompressedImageSize === 0) {
          this.getUIContext().showAlertDialog({
            message: $r('app.string.prompt_enter_value_greater_than_0'),
            alignment: DialogAlignment.Center
          });
          return;
        }
        if (this.maxCompressedImageSize * CommonConstants.BYTE_CONVERSION > this.sourceImageByteLength) {
          if (this.sourceImageByteLength === 0) {
            this.getUIContext().showAlertDialog({
              message: $r('app.string.image_get_failed'),
              alignment: DialogAlignment.Center
            });
          } else {
            this.getUIContext().showAlertDialog({
              message: $r('app.string.prompt_not_require_compression'),
              alignment: DialogAlignment.Center
            });
          }
          return;
        }
        this.compressedImageSrc = '';
        this.imageCompression();
      }).fontSize($r('app.float.font_size_16')).width($r('app.string.button_width'))

      Row() {
        Text($r('app.string.image_size_before_compression'))
          .fontSize($r('app.float.font_size_16'))
        Text(this.beforeCompressionSize)
          .fontSize($r('app.float.font_size_16'))
      }

      Image($rawfile('compression.jpeg'))
        .width($r('app.string.image_width'))
        .height($r('app.string.image_height'))

      Row() {
        Text($r('app.string.image_size_after_compression'))
          .fontSize($r('app.float.font_size_16'))
        Text(this.afterCompressionSize)
          .fontSize($r('app.float.font_size_16'))
      }

      Image(this.compressedImageSrc)
        .width($r('app.string.image_width'))
        .height($r('app.string.image_height'))
    }.alignItems(HorizontalAlign.Start).padding($r('app.float.column_padding'))
  }
}




/*
 * Copyright (c) 2024 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

// import { BusinessError } from '@kit.BasicServicesKit';
// import { fileIo, fileUri } from '@kit.CoreFileKit';
// import { image } from '@kit.ImageKit';
// import { hilog } from '@kit.PerformanceAnalysisKit';
// import CommonConstants from '../common/CommonConstants';
//
// const TAG = 'IMAGE_COMPRESSION';
//
// class CompressedImageInfo {
//   imageUri: string = "";
//   imageByteLength: number = 0;
//   actualQuality: number = 0; // 新增：记录实际使用的质量参数
// }
//
// /**
//  * 创建图片打包器实例
//  */
// function createImagePacker(): image.ImagePacker {
//   return image.createImagePacker();
// }
//
// /**
//  * 统一的图片打包方法
//  */
// async function packImage(sourcePixelMap: image.PixelMap, imageQuality: number): Promise<ArrayBuffer> {
//   const imagePacker = createImagePacker();
//   const packOpts: image.PackingOption = {
//     format: "image/jpeg",
//     quality: imageQuality
//   };
//
//   try {
//     return await imagePacker.packToData(sourcePixelMap, packOpts);
//   } catch (error) {
//     const businessError = error as BusinessError;
//     hilog.error(0x0000, TAG, `Image packing failed, code: ${businessError.code}, message: ${businessError.message}`);
//     throw new Error(`图片压缩失败: ${businessError.message}`);
//   }
// }
//
// /**
//  * 优化版二分法图片压缩 - 核心算法改进
//  */
// async function compressedImage(
//   sourcePixelMap: image.PixelMap,
//   maxCompressedImageSize: number
// ): Promise<CompressedImageInfo> {
//   const maxCompressedImageByte = maxCompressedImageSize * CommonConstants.BYTE_CONVERSION;
//   const tolerance = maxCompressedImageByte * CommonConstants.COMPRESSION_TOLERANCE;
//
//   hilog.info(0x0000, TAG, `开始压缩，目标大小: ${maxCompressedImageByte} bytes, 容忍度: ±${tolerance} bytes`);
//
//   // 1. 先用最高质量测试，了解图片的基线大小
//   const maxQualityData = await packImage(sourcePixelMap, CommonConstants.PICTURE_QUALITY_MAX);
//   if (maxQualityData.byteLength <= maxCompressedImageByte) {
//     hilog.info(0x0000, TAG, '最高质量已满足要求，无需压缩');
//     return await saveImage(maxQualityData, CommonConstants.PICTURE_QUALITY_MAX);
//   }
//
//   // 2. 用最低质量测试，确定压缩下限
//   const minQualityData = await packImage(sourcePixelMap, 0);
//   if (minQualityData.byteLength > maxCompressedImageByte) {
//     hilog.info(0x0000, TAG, '最低质量仍超过目标，启用尺寸缩放');
//     return await scaleAndCompress(sourcePixelMap, maxCompressedImageByte);
//   }
//
//   // 3. 二分法寻找最优质量参数
//   const optimalQuality = await findOptimalQuality(
//     sourcePixelMap,
//     maxCompressedImageByte,
//     tolerance
//   );
//
//   const finalData = await packImage(sourcePixelMap, optimalQuality);
//   hilog.info(0x0000, TAG, `压缩完成，质量: ${optimalQuality}, 大小: ${finalData.byteLength} bytes`);
//
//   return await saveImage(finalData, optimalQuality);
// }
//
// /**
//  * 优化的二分法质量查找 - 解决"差距大"的问题
//  */
// async function findOptimalQuality(
//   sourcePixelMap: image.PixelMap,
//   targetSize: number,
//   tolerance: number
// ): Promise<number> {
//   let low = 0;
//   let high = CommonConstants.PICTURE_QUALITY_MAX;
//   let bestQuality = low;
//   let bestSize = 0;
//
//   // 生成更精细的质量数组
//   const qualitySteps: number[] = [];
//   for (let i = low; i <= high; i += CommonConstants.DICHOTOMY_ACCURACY) {
//     qualitySteps.push(i);
//   }
//
//   hilog.info(0x0000, TAG, `开始二分法搜索，质量范围: [${low}, ${high}]，步长: ${CommonConstants.DICHOTOMY_ACCURACY}`);
//
//   while (low <= high) {
//     const mid = Math.floor((low + high) / 2);
//     const currentQuality = qualitySteps[mid];
//
//     const currentData = await packImage(sourcePixelMap, currentQuality);
//     const currentSize = currentData.byteLength;
//
//     hilog.info(0x0000, TAG, `质量 ${currentQuality} → 大小 ${currentSize} bytes`);
//
//     // 关键优化：记录最接近目标的最佳结果
//     if (currentSize <= targetSize) {
//       if (currentSize > bestSize) {
//         bestSize = currentSize;
//         bestQuality = currentQuality;
//       }
//
//       // 如果在容忍范围内，直接返回
//       if (currentSize >= targetSize - tolerance) {
//         hilog.info(0x0000, TAG, `找到满意质量: ${currentQuality}, 大小: ${currentSize}`);
//         return currentQuality;
//       }
//       low = mid + 1; // 尝试更高质量
//     } else {
//       high = mid - 1; // 当前质量过大，降低质量
//     }
//   }
//
//   // 返回找到的最佳质量（最接近但不超过目标）
//   hilog.info(0x0000, TAG, `返回最佳质量: ${bestQuality}, 大小: ${bestSize}`);
//   return bestQuality;
// }
//
// /**
//  * 尺寸缩放压缩 - 当质量压缩无法满足时的备选方案
//  */
// async function scaleAndCompress(
//   sourcePixelMap: image.PixelMap,
//   targetSize: number
// ): Promise<CompressedImageInfo> {
//   let imageScale = 1.0;
//   const minScale = CommonConstants.MIN_SCALE_LIMIT;
//
//   hilog.info(0x0000, TAG, `开始尺寸缩放，初始缩放比例: ${imageScale}`);
//
//   while (imageScale >= minScale) {
//     // 先缩放
//     imageScale = Math.max(minScale, imageScale - CommonConstants.REDUCE_SCALE);
//     await sourcePixelMap.scale(imageScale, imageScale);
//
//     // 用最低质量测试
//     const testData = await packImage(sourcePixelMap, 0);
//
//     if (testData.byteLength <= targetSize) {
//       // 缩放后满足要求，用二分法找最佳质量
//       const optimalQuality = await findOptimalQuality(sourcePixelMap, targetSize, targetSize * 0.05);
//       const finalData = await packImage(sourcePixelMap, optimalQuality);
//
//       hilog.info(0x0000, TAG, `缩放完成，最终比例: ${imageScale}, 质量: ${optimalQuality}`);
//       return await saveImage(finalData, optimalQuality);
//     }
//
//     hilog.info(0x0000, TAG, `缩放至 ${imageScale}，大小: ${testData.byteLength}，继续缩放...`);
//   }
//
//   // 缩放至最小仍不满足，返回最小尺寸的结果
//   const finalData = await packImage(sourcePixelMap, 0);
//   hilog.warn(0x0000, TAG, `已缩放至最小限制，使用最低质量`);
//   return await saveImage(finalData, 0);
// }
//
// /**
//  * 增强的文件保存方法
//  */
// async function saveImage(compressedImageData: ArrayBuffer, qualityUsed: number): Promise<CompressedImageInfo> {
//   const uiContext: UIContext | undefined = AppStorage.get('uiContext');
//   if (!uiContext) {
//     throw new Error('UIContext 未找到，无法保存图片');
//   }
//
//   const context: Context = uiContext.getHostContext()!;
//   const timestamp = new Date().getTime();
//   const filename = `compressed_${timestamp}_q${qualityUsed}.png`;
//   const compressedImageUri: string = `${context.filesDir}/${filename}`;
//
//   try {
//     // 检查并删除已存在的文件
//     if (fileIo.accessSync(compressedImageUri)) {
//       fileIo.unlinkSync(compressedImageUri);
//     }
//
//     // 写入文件
//     const file = fileIo.openSync(compressedImageUri,
//       fileIo.OpenMode.READ_WRITE | fileIo.OpenMode.CREATE);
//     fileIo.writeSync(file.fd, compressedImageData);
//     fileIo.closeSync(file);
//
//     hilog.info(0x0000, TAG, `图片保存成功: ${compressedImageUri}`);
//
//     const compressedImageInfo = new CompressedImageInfo();
//     compressedImageInfo.imageUri = compressedImageUri;
//     compressedImageInfo.imageByteLength = compressedImageData.byteLength;
//     compressedImageInfo.actualQuality = qualityUsed;
//
//     return compressedImageInfo;
//
//   } catch (err) {
//     hilog.error(0x0000, TAG, `文件保存失败: ${JSON.stringify(err)}`);
//     throw new Error(`文件保存失败: ${err.message}`);
//   }
// }
//
// export { compressedImage, CompressedImageInfo };
//
//
//
// @Entry
// @Component
// struct Index {
//   @State compressedImageSrc: string | Resource = '';
//   @State beforeCompressionSize: string = '';
//   @State afterCompressionSize: string = '';
//   @State actualQualityUsed: number = 0; // 新增：显示实际质量参数
//   @State isCompressing: boolean = false; // 新增：压缩状态
//
//   private sourceImageByteLength: number = 0;
//   private compressedByteLength: number = 0;
//   private maxCompressedImageSize: number = 0;
//
//   aboutToAppear(): void {
//     this.loadOriginalImageInfo();
//   }
//
//   private loadOriginalImageInfo(): void {
//     const context: Context = this.getUIContext().getHostContext()!;
//     const resourceMgr = context.resourceManager;
//
//     resourceMgr.getRawFileContent('beforeCompression.jpeg').then((fileData: Uint8Array) => {
//       this.sourceImageByteLength = fileData.buffer.byteLength;
//       this.beforeCompressionSize = (this.sourceImageByteLength / CommonConstants.BYTE_CONVERSION).toFixed(1);
//     }).catch((err: BusinessError) => {
//       hilog.error(0x0000, TAG, `原始图片加载失败: ${JSON.stringify(err)}`);
//       this.showErrorDialog($r('app.string.image_get_failed').toString());
//     });
//   }
//
//   async imageCompression(): Promise<void> {
//     if (this.isCompressing) {
//       return; // 防止重复点击
//     }
//
//     this.isCompressing = true;
//     this.compressedImageSrc = '';
//
//     try {
//       const context = this.getUIContext().getHostContext()!;
//       const resourceMgr = context.resourceManager;
//
//       const fileData: Uint8Array = await resourceMgr.getRawFileContent('beforeCompression.jpeg');
//       const buffer = fileData.buffer.slice(0);
//
//       const imageSource = image.createImageSource(buffer);
//       const decodingOptions: image.DecodingOptions = {
//         editable: true,
//         desiredPixelFormat: 3,
//       };
//
//       const originalPixelMap = await imageSource.createPixelMap(decodingOptions);
//       const showImage = await compressedImage(originalPixelMap, this.maxCompressedImageSize);
//
//       // 更新UI
//       this.compressedImageSrc = fileUri.getUriFromPath(showImage.imageUri);
//       this.compressedByteLength = showImage.imageByteLength;
//       this.afterCompressionSize = (this.compressedByteLength / CommonConstants.BYTE_CONVERSION).toFixed(1);
//       this.actualQualityUsed = showImage.actualQuality;
//
//       // 资源释放
//       originalPixelMap.release();
//       imageSource.release();
//
//     } catch (err) {
//       hilog.error(0x0000, TAG, `压缩过程错误: ${JSON.stringify(err)}`);
//       this.showErrorDialog('图片压缩失败，请重试');
//     } finally {
//       this.isCompressing = false;
//     }
//   }
//
//   private showErrorDialog(message: string): void {
//     this.getUIContext().showAlertDialog({
//       message: message,
//       alignment: DialogAlignment.Center
//     });
//   }
//
//   private validateInput(): boolean {
//     if (this.maxCompressedImageSize === 0) {
//       this.showErrorDialog($r('app.string.prompt_enter_value_greater_than_0').toString());
//       return false;
//     }
//
//     const targetBytes = this.maxCompressedImageSize * CommonConstants.BYTE_CONVERSION;
//     if (targetBytes > this.sourceImageByteLength) {
//       if (this.sourceImageByteLength === 0) {
//         this.showErrorDialog($r('app.string.image_get_failed').toString());
//       } else {
//         this.showErrorDialog($r('app.string.prompt_not_require_compression').toString());
//       }
//       return false;
//     }
//
//     return true;
//   }
//
//   build() {
//     Column({ space: CommonConstants.SPACE_TEN }) {
//       // 输入区域
//       Row({ space: CommonConstants.SPACE_TEN }) {
//         Text($r('app.string.max_compression_image_size'))
//           .fontSize($r('app.float.font_size_16'))
//         TextInput()
//           .type(InputType.Number)
//           .fontSize($r('app.float.font_size_16'))
//           .width($r('app.string.text_input_width'))
//           .onChange((value: string) => {
//             this.maxCompressedImageSize = Number.parseInt(value) || 0;
//           })
//       }
//
//       // 压缩按钮
//       Button($r('app.string.image_compression'))
//         .onClick(() => {
//           if (this.validateInput()) {
//             this.imageCompression();
//           }
//         })
//         .fontSize($r('app.float.font_size_16'))
//         .width($r('app.string.button_width'))
//         .enabled(!this.isCompressing)
//
//       // 压缩前信息
//       Row() {
//         Text($r('app.string.image_size_before_compression'))
//           .fontSize($r('app.float.font_size_16'))
//         Text(this.beforeCompressionSize)
//           .fontSize($r('app.float.font_size_16'))
//       }
//
//       Image($rawfile('beforeCompression.jpeg'))
//         .width($r('app.string.image_width'))
//         .height($r('app.string.image_height'))
//
//       // 压缩后信息
//       Row() {
//         Text($r('app.string.image_size_after_compression'))
//           .fontSize($r('app.float.font_size_16'))
//         Text(this.afterCompressionSize)
//           .fontSize($r('app.float.font_size_16'))
//       }
//
//       // 实际质量显示（新增）
//       Row() {
//         Text('实际压缩质量:')
//           .fontSize($r('app.float.font_size_16'))
//         Text(this.actualQualityUsed.toString())
//           .fontSize($r('app.float.font_size_16'))
//           .fontColor(Color.Blue)
//       }
//
//       Image(this.compressedImageSrc)
//         .width($r('app.string.image_width'))
//         .height($r('app.string.image_height'))
//
//       // 加载指示器
//       if (this.isCompressing) {
//         LoadingProgress()
//           .color(Color.Blue)
//           .width(50)
//           .height(50)
//       }
//
//     }.alignItems(HorizontalAlign.Start).padding($r('app.float.column_padding'))
//   }
// }