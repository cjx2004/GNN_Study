# demo.py

### 启动AI2-THOR模拟器
```python
from ai2thor.controller import Controller

controller = Controller(
    scene = "FloorPlan221",
    gridSize = 0.25,
    rotateStepDegrees = 90,
    renderDepthImage = True,
    renderInstanceSegmentation = True,
    fieldOfView = 90
)
```

### 动作

#### 传送动作
支持将智能体传送至当前场景中的指定位置。
`GetReachablePositions`动作可以获取当前场景中智能体的可行位置列表。
```python
event = controller.step(action = "GetReachablePositions")
reachable_positions = event.metadata["actionReturn"]
```

`Teleport`动作可以将智能体直接传送至场景中的指定位置。
```python
event = controller.step(
    action = "Teleport",
    position = dict(x = -3.00, y = 0.9984914064407349, z = -2.25),
    rotation = dict(x = 0, y = 0, z = 0),
    horizon = 0,
    standing = True
)
```

#### 移动动作
支持的移动动作包括 `MoveAhead`, `MoveBack`, `MoveRight`, `MoveLeft`，分别为向前、向后、向右、向左移动`gridSize`距离。执行移动动作时，智能体的朝向不会发生改变。
```python
controller.step("MoveAhead")
controller.step("MoveBack")
controller.step("MoveRight")
controller.step("MoveLeft")
```

#### 旋转动作
支持的旋转动作包括 `RotateRight`, `RotateLeft`, 分别为向右旋转、向左旋转`rotateStepDegrees`度。执行旋转动作时，智能体位置不会发生变化。
```python
controller.step("RotateRight")
controller.step("RotateLeft")
```

#### 操作动作
支持的常见操作动作包括 `PickupObject`, `PutObject`, 分别为拿起、放下某物体。
执行`PickUpObject`动作时，参数`objectId`为被拿起物体在场景中的id，要求被拿起物体必须具有`pickupable`属性，并且当前智能体所在位置必须与该物体可交互才能执行成功。动作返回值`event.metadata["lastActionSuccess"]`表示当前动作执行是否成功。
```python
event = controller.step(
    action = "PickupObject",
    objectId = "Plate|-03.85|+00.88|-01.01"
)
print("PickUp Plate {}".format(event.metadata["lastActionSuccess"]))
```

执行`PutObject`动作时，参数`objectId`为被拿起物体被放置于的物体id，要求智能体当前必须已经拿起某物体，将被拿起物体放置于的物体必须为`receptacle`类物体。
```python
event = controller.step(
    action = "PutObject",
    objectId = "CoffeeTable|-01.09|+00.10|-00.74"
)
print("Put Plate to CoffeeTable {}".format(event.metadata["lastActionSuccess"]))
```

### 状态

#### 第一视角观测
智能体执行完动作后，可以保存其当前状态，包括第一视角的RGB观测。
```python
plt.imsave('first_view.png', event.frame)
```

#### Top-Down观测
通过动作`GetMapViewCameraProperties`与动作`AddThirdPartyCamera`结合可以生成当前场景下的俯视图(Top-Down)
```python
event = controller.step(action = "GetMapViewCameraProperties", raise_for_failure = True)
event = controller.step(
    action = "AddThirdPartyCamera",
    **event.metadata["actionReturn"]
)
top_down_frame = event.third_party_camera_frames[-1]
plt.imsave('top_down.png', top_down_frame)
```

### 平台使用样例
demo.py文件中包含了对智能体在场景中的常见导航及操作动作，执行该文件可以生成智能体每一步动作的第一视角观测图像和执行完成后的Top-Down图像。
