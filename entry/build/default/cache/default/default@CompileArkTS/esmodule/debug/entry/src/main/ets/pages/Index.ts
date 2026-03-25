if (!("finalizeConstruction" in ViewPU.prototype)) {
    Reflect.set(ViewPU.prototype, "finalizeConstruction", () => { });
}
interface Index_Params {
    compressedImageSrc?: string | Resource;
    beforeCompressionSize?: string;
    afterCompressionSize?: string;
    sourceImageByteLength?: number;
    compressedByteLength?: number;
    maxCompressedImageSize?: number;
    context?: Context;
}
import type { BusinessError as BusinessError } from "@ohos:base";
import fileIo from "@ohos:file.fs";
import fileUri from "@ohos:file.fileuri";
import image from "@ohos:multimedia.image";
import type resourceManager from "@ohos:resourceManager";
import hilog from "@ohos:hilog";
import CommonConstants from "@bundle:com.example.imagecompression/entry/ets/common/CommonConstants";
const TAG = 'IMAGE_COMPRESSION';
class CompressedImageInfo {
    imageUri: string = "";
    imageByteLength: number = 0;
}
async function compressedImage(sourcePixelMap: image.PixelMap, maxCompressedImageSize: number): Promise<CompressedImageInfo> {
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
    }
    else {
        let imageScale = 1;
        const REDUCE_SCALE = CommonConstants.REDUCE_SCALE;
        while (compressedImageData.byteLength > maxCompressedImageByte) {
            if (imageScale > 0) {
                imageScale = imageScale - REDUCE_SCALE;
                await sourcePixelMap.scale(imageScale, imageScale);
                compressedImageData = await packing(sourcePixelMap, IMAGE_QUALITY);
            }
            else {
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
async function packingImage(compressedImageData: ArrayBuffer, sourcePixelMap: image.PixelMap, imageQuality: number, maxCompressedImageByte: number): Promise<ArrayBuffer> {
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
        }
        else {
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
    }
    catch (err) {
        hilog.error(0x0000, TAG, JSON.stringify(err));
    }
    let compressedImageInfo: CompressedImageInfo = new CompressedImageInfo();
    compressedImageInfo.imageUri = compressedImageUri;
    compressedImageInfo.imageByteLength = compressedImageData.byteLength;
    return compressedImageInfo;
}
class Index extends ViewPU {
    constructor(parent, params, __localStorage, elmtId = -1, paramsLambda = undefined, extraInfo) {
        super(parent, __localStorage, elmtId, extraInfo);
        if (typeof paramsLambda === "function") {
            this.paramsGenerator_ = paramsLambda;
        }
        this.__compressedImageSrc = new ObservedPropertyObjectPU('', this, "compressedImageSrc");
        this.__beforeCompressionSize = new ObservedPropertySimplePU('', this, "beforeCompressionSize");
        this.__afterCompressionSize = new ObservedPropertySimplePU('', this, "afterCompressionSize");
        this.sourceImageByteLength = 0;
        this.compressedByteLength = 0;
        this.maxCompressedImageSize = 0;
        this.context = this.getUIContext().getHostContext()!;
        this.setInitiallyProvidedValue(params);
        this.finalizeConstruction();
    }
    setInitiallyProvidedValue(params: Index_Params) {
        if (params.compressedImageSrc !== undefined) {
            this.compressedImageSrc = params.compressedImageSrc;
        }
        if (params.beforeCompressionSize !== undefined) {
            this.beforeCompressionSize = params.beforeCompressionSize;
        }
        if (params.afterCompressionSize !== undefined) {
            this.afterCompressionSize = params.afterCompressionSize;
        }
        if (params.sourceImageByteLength !== undefined) {
            this.sourceImageByteLength = params.sourceImageByteLength;
        }
        if (params.compressedByteLength !== undefined) {
            this.compressedByteLength = params.compressedByteLength;
        }
        if (params.maxCompressedImageSize !== undefined) {
            this.maxCompressedImageSize = params.maxCompressedImageSize;
        }
        if (params.context !== undefined) {
            this.context = params.context;
        }
    }
    updateStateVars(params: Index_Params) {
    }
    purgeVariableDependenciesOnElmtId(rmElmtId) {
        this.__compressedImageSrc.purgeDependencyOnElmtId(rmElmtId);
        this.__beforeCompressionSize.purgeDependencyOnElmtId(rmElmtId);
        this.__afterCompressionSize.purgeDependencyOnElmtId(rmElmtId);
    }
    aboutToBeDeleted() {
        this.__compressedImageSrc.aboutToBeDeleted();
        this.__beforeCompressionSize.aboutToBeDeleted();
        this.__afterCompressionSize.aboutToBeDeleted();
        SubscriberManager.Get().delete(this.id__());
        this.aboutToBeDeletedInternal();
    }
    private __compressedImageSrc: ObservedPropertyObjectPU<string | Resource>;
    get compressedImageSrc() {
        return this.__compressedImageSrc.get();
    }
    set compressedImageSrc(newValue: string | Resource) {
        this.__compressedImageSrc.set(newValue);
    }
    private __beforeCompressionSize: ObservedPropertySimplePU<string>;
    get beforeCompressionSize() {
        return this.__beforeCompressionSize.get();
    }
    set beforeCompressionSize(newValue: string) {
        this.__beforeCompressionSize.set(newValue);
    }
    private __afterCompressionSize: ObservedPropertySimplePU<string>;
    get afterCompressionSize() {
        return this.__afterCompressionSize.get();
    }
    set afterCompressionSize(newValue: string) {
        this.__afterCompressionSize.set(newValue);
    }
    private sourceImageByteLength: number;
    private compressedByteLength: number;
    private maxCompressedImageSize: number;
    private context: Context;
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
            };
            imageSource.createPixelMap(decodingOptions).then((originalPixelMap: image.PixelMap) => {
                compressedImage(originalPixelMap, this.maxCompressedImageSize).then((showImage: CompressedImageInfo) => {
                    this.compressedImageSrc = fileUri.getUriFromPath(showImage.imageUri);
                    this.compressedByteLength = showImage.imageByteLength;
                    this.afterCompressionSize = (this.compressedByteLength / CommonConstants.BYTE_CONVERSION).toFixed(1);
                });
            }).catch((err: BusinessError) => {
                hilog.error(0x0000, TAG, JSON.stringify(err));
            });
        }).catch((err: BusinessError) => {
            hilog.error(0x0000, TAG, JSON.stringify(err));
        });
    }
    initialRender() {
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Column.create({ space: CommonConstants.SPACE_TEN });
            Column.alignItems(HorizontalAlign.Start);
            Column.padding({ "id": 16777233, "type": 10002, params: [], "bundleName": "com.example.imagecompression", "moduleName": "entry" });
        }, Column);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Row.create({ space: CommonConstants.SPACE_TEN });
        }, Row);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Text.create({ "id": 16777227, "type": 10003, params: [], "bundleName": "com.example.imagecompression", "moduleName": "entry" });
            Text.fontSize({ "id": 16777234, "type": 10002, params: [], "bundleName": "com.example.imagecompression", "moduleName": "entry" });
        }, Text);
        Text.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            TextInput.create();
            TextInput.type(InputType.Number);
            TextInput.fontSize({ "id": 16777234, "type": 10002, params: [], "bundleName": "com.example.imagecompression", "moduleName": "entry" });
            TextInput.width({ "id": 16777231, "type": 10003, params: [], "bundleName": "com.example.imagecompression", "moduleName": "entry" });
            TextInput.onChange((value: string) => {
                this.maxCompressedImageSize = Number(value);
            });
        }, TextInput);
        Row.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Button.createWithLabel({ "id": 16777221, "type": 10003, params: [], "bundleName": "com.example.imagecompression", "moduleName": "entry" });
            Button.onClick(() => {
                if (this.maxCompressedImageSize === 0) {
                    this.getUIContext().showAlertDialog({
                        message: { "id": 16777229, "type": 10003, params: [], "bundleName": "com.example.imagecompression", "moduleName": "entry" },
                        alignment: DialogAlignment.Center
                    });
                    return;
                }
                if (this.maxCompressedImageSize * CommonConstants.BYTE_CONVERSION > this.sourceImageByteLength) {
                    if (this.sourceImageByteLength === 0) {
                        this.getUIContext().showAlertDialog({
                            message: { "id": 16777222, "type": 10003, params: [], "bundleName": "com.example.imagecompression", "moduleName": "entry" },
                            alignment: DialogAlignment.Center
                        });
                    }
                    else {
                        this.getUIContext().showAlertDialog({
                            message: { "id": 16777230, "type": 10003, params: [], "bundleName": "com.example.imagecompression", "moduleName": "entry" },
                            alignment: DialogAlignment.Center
                        });
                    }
                    return;
                }
                this.compressedImageSrc = '';
                this.imageCompression();
            });
            Button.fontSize({ "id": 16777234, "type": 10002, params: [], "bundleName": "com.example.imagecompression", "moduleName": "entry" });
            Button.width({ "id": 16777220, "type": 10003, params: [], "bundleName": "com.example.imagecompression", "moduleName": "entry" });
        }, Button);
        Button.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Row.create();
        }, Row);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Text.create({ "id": 16777225, "type": 10003, params: [], "bundleName": "com.example.imagecompression", "moduleName": "entry" });
            Text.fontSize({ "id": 16777234, "type": 10002, params: [], "bundleName": "com.example.imagecompression", "moduleName": "entry" });
        }, Text);
        Text.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Text.create(this.beforeCompressionSize);
            Text.fontSize({ "id": 16777234, "type": 10002, params: [], "bundleName": "com.example.imagecompression", "moduleName": "entry" });
        }, Text);
        Text.pop();
        Row.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Image.create({ "id": 0, "type": 30000, params: ['compression.jpeg'], "bundleName": "com.example.imagecompression", "moduleName": "entry" });
            Image.width({ "id": 16777226, "type": 10003, params: [], "bundleName": "com.example.imagecompression", "moduleName": "entry" });
            Image.height({ "id": 16777223, "type": 10003, params: [], "bundleName": "com.example.imagecompression", "moduleName": "entry" });
        }, Image);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Row.create();
        }, Row);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Text.create({ "id": 16777224, "type": 10003, params: [], "bundleName": "com.example.imagecompression", "moduleName": "entry" });
            Text.fontSize({ "id": 16777234, "type": 10002, params: [], "bundleName": "com.example.imagecompression", "moduleName": "entry" });
        }, Text);
        Text.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Text.create(this.afterCompressionSize);
            Text.fontSize({ "id": 16777234, "type": 10002, params: [], "bundleName": "com.example.imagecompression", "moduleName": "entry" });
        }, Text);
        Text.pop();
        Row.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Image.create(this.compressedImageSrc);
            Image.width({ "id": 16777226, "type": 10003, params: [], "bundleName": "com.example.imagecompression", "moduleName": "entry" });
            Image.height({ "id": 16777223, "type": 10003, params: [], "bundleName": "com.example.imagecompression", "moduleName": "entry" });
        }, Image);
        Column.pop();
    }
    rerender() {
        this.updateDirtyElements();
    }
    static getEntryName(): string {
        return "Index";
    }
}
registerNamedRoute(() => new Index(undefined, {}), "", { bundleName: "com.example.imagecompression", moduleName: "entry", pagePath: "pages/Index", pageFullPath: "entry/src/main/ets/pages/Index", integratedHsp: "false", moduleType: "followWithHap" });
