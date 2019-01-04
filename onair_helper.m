//
//  main.m
//  onair_helper
//
// Adapted from Patrick Wardle's code as demoed here:
// https://www.youtube.com/watch?v=5C0CPxwEAz8
//

#import <Foundation/Foundation.h>
#import <AVFoundation/AVFoundation.h>
#import <CoreMediaIO/CMIOHardwareObject.h>

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        NSArray *cameras = nil;
        cameras = [AVCaptureDevice devicesWithMediaType:AVMediaTypeVideo];
        for(AVCaptureDevice* camera in cameras)
        {
            printf("Found camera: %s/%s\n", [camera.manufacturer UTF8String], [camera.localizedName UTF8String]);
            UInt32 connectionID = (UInt32) [camera performSelector:NSSelectorFromString(@"connectionID") withObject:nil];
            CMIOObjectPropertyAddress propertyStruct = {0};
            propertyStruct.mSelector = kAudioDevicePropertyDeviceIsRunningSomewhere;
            propertyStruct.mScope = kAudioObjectPropertyScopeGlobal;
            propertyStruct.mElement = kAudioObjectPropertyElementMaster;
            CMIOObjectPropertyListenerBlock listenerBlock =
            ^(UInt32 inNumberAddresses, const CMIOObjectPropertyAddress addresses[])
            {
                UInt32 isRunning = -1;
                UInt32 propertySize = sizeof(isRunning);
                CMIOObjectPropertyAddress propertyStruct = {0};
                propertyStruct.mSelector = kAudioDevicePropertyDeviceIsRunningSomewhere;
                propertyStruct.mScope = kAudioObjectPropertyScopeGlobal;
                propertyStruct.mElement = kAudioObjectPropertyElementMaster;
                CMIOObjectGetPropertyData(connectionID, &propertyStruct, 0, NULL,
                                          sizeof(kAudioDevicePropertyDeviceIsRunningSomewhere), &propertySize, &isRunning);
                if(YES == isRunning)
                {
                    printf("Camera active\n");
                } else {
                    printf("Camera inactive\n");
                }

            };
            CMIOObjectAddPropertyListenerBlock(connectionID, &propertyStruct, dispatch_get_main_queue(), listenerBlock);

        }
        [[NSRunLoop currentRunLoop] run];
    }
    return 0;
}
