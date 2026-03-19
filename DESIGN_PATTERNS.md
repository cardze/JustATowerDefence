# 塔防遊戲設計模式重構指南

本文档详细介绍了如何在塔防游戏中应用四个主要的设计模式。

## 目录
1. [策略模式 (Strategy Pattern)](#策略模式)
2. [状态模式 (State Pattern)](#状态模式)
3. [观察者模式 (Observer Pattern)](#观察者模式)
4. [建造者模式 (Builder Pattern)](#建造者模式)

---

## 策略模式

### 概述
策略模式允许塔在运行时动态改变其攻击策略，而无需修改塔的代码。

### 文件
- **tower_defence/combat/attack_strategy.py**: 定义了所有攻击策略

### 实现的策略

#### 1. 最近敌人策略 (ClosestEnemyStrategy)
```python
strategy = ClosestEnemyStrategy()
tower.set_attack_strategy(strategy)
```
- 攻击范围内最接近的敌人
- 适用于基础塔

#### 2. 最快敌人策略 (FastestEnemyStrategy)
```python
strategy = FastestEnemyStrategy()
tower.set_attack_strategy(strategy)
```
- 攻击范围内速度最快的敌人
- 适用于快速射击塔 (Rapid Tower)

#### 3. 最强敌人策略 (StrongestEnemyStrategy)
```python
strategy = StrongestEnemyStrategy()
tower.set_attack_strategy(strategy)
```
- 攻击范围内血量最多的敌人
- 适用于狙击塔 (Sniper Tower)

#### 4. 最远敌人策略 (FarthestEnemyStrategy)
```python
strategy = FarthestEnemyStrategy()
tower.set_attack_strategy(strategy)
```
- 攻击路径上最先进的敌人
- 适用于防守后方的塔

### 用法示例
```python
# 创建塔
tower = Tower(100, 100, 'basic')

# 改变攻击策略
tower.set_attack_strategy(StrongestEnemyStrategy())

# 策略会自动用于攻击计算
projectile = tower.update(enemies)
```

### 优势
- ✅ 易于添加新的策略
- ✅ 运行时动态切换策略
- ✅ 解耦攻击逻辑与塔的实现
- ✅ 便于测试和维护

---

## 状态模式

### 概述
状态模式用于管理塔的不同状态，每个状态有不同的行为。

### 文件
- **tower_defence/towers/tower_state.py**: 定义了塔的所有状态

### 实现的状态

#### 1. 闲置状态 (IdleState)
```python
from tower_defence.towers.tower_state import IdleState
tower.set_state(IdleState())
```
- 塔正在搜索目标
- 没有敌人在范围内时的状态

#### 2. 攻击状态 (AttackingState)
```python
from tower_defence.towers.tower_state import AttackingState
tower.set_state(AttackingState())
```
- 塔正在主动攻击目标
- 有敌人在范围内的状态

#### 3. 升级状态 (UpgradedState)
```python
from tower_defence.towers.tower_state import UpgradedState
tower.set_state(UpgradedState())
```
- 塔已被升级
- 具有增强属性的状态

#### 4. 冷却状态 (CooldownState)
```python
from tower_defence.towers.tower_state import CooldownState
tower.set_state(CooldownState(cooldown_frames=10))
```
- 塔在冷却中
- 暂时无法射击

### 用法示例
```python
# 塔的状态自动管理
tower = Tower(100, 100, 'basic')

# 升级后自动转换到升级状态
tower.upgrade()  # 状态变为 UpgradedState

# 手动改变状态
tower.set_state(AttackingState())
print(tower.state.get_state_name())  # "Attacking"
```

### 优势
- ✅ 清晰的状态管理
- ✅ 状态间的平滑过渡
- ✅ 易于调试和理解塔的行为
- ✅ 便于添加新状态

---

## 观察者模式

### 概述
观察者模式实现了事件驱动的架构，允许游戏组件对重要事件做出反应。

### 文件
- **tower_defence/systems/event_system.py**: 定义了事件管理系统

### 核心组件

#### EventManager (事件管理器)
中央事件总线，管理所有事件的发射和订阅。

```python
from tower_defence.systems.event_system import EventManager, GameEvent

event_manager = EventManager()

# 订阅事件
def on_enemy_killed(event, data):
    print(f"Enemy killed! Reward: {data['reward']}")

event_manager.subscribe_callback(GameEvent.ENEMY_KILLED, on_enemy_killed)

# 发射事件
event_manager.emit(GameEvent.ENEMY_KILLED, {'reward': 10})
```

### 支持的事件

| 事件 | 描述 | 发生时机 |
|------|------|---------|
| ENEMY_SPAWNED | 敌人生成 | 敌人进入游戏 |
| ENEMY_KILLED | 敌人被击杀 | 敌人血量 <= 0 |
| ENEMY_ESCAPED | 敌人逃脱 | 敌人到达终点 |
| TOWER_PLACED | 塔被放置 | 塔添加到游戏 |
| TOWER_UPGRADED | 塔被升级 | 塔升级成功 |
| TOWER_SOLD | 塔被售出 | 塔从游戏中移除 |
| ENEMY_IN_RANGE | 敌人进入范围 | 敌人进入塔的攻击范围 |
| ENEMY_OUT_OF_RANGE | 敌人离开范围 | 敌人离开塔的攻击范围 |
| WAVE_STARTED | 波次开始 | 新的敌人波次开始 |
| WAVE_COMPLETED | 波次完成 | 所有敌人被消灭或逃脱 |
| GAME_OVER | 游戏结束 | 玩家生命值 <= 0 |
| MONEY_CHANGED | 金钱变化 | 金钱增加或减少 |
| LIVES_CHANGED | 生命值变化 | 生命值增加或减少 |

### 观察者实现

#### 1. 游戏事件观察者
```python
from tower_defence.systems.event_system import GameEventObserver

observer = GameEventObserver("Game Logger")
event_manager.subscribe(GameEvent.TOWER_PLACED, observer)
```

#### 2. UI事件观察者
```python
from tower_defence.systems.event_system import UIEventObserver

ui_observer = UIEventObserver(ui)
event_manager.subscribe(GameEvent.MONEY_CHANGED, ui_observer)
event_manager.subscribe(GameEvent.LIVES_CHANGED, ui_observer)
```

### 用法示例
```python
from tower_defence.systems.event_system import EventManager, GameEvent

# 创建事件管理器
events = EventManager()

# 订阅事件
def handle_wave_completed(event, data):
    print(f"Wave {data['wave']} completed!")
    print(f"Money: ${data['money']}")

events.subscribe_callback(GameEvent.WAVE_COMPLETED, handle_wave_completed)

# 发射事件
events.emit(GameEvent.WAVE_COMPLETED, {
    'wave': 5,
    'money': 500
})
```

### 优势
- ✅ 组件间解耦
- ✅ 易于添加新的观察者
- ✅ 灵活的事件处理
- ✅ 便于日志记录和调试

---

## 建造者模式

### 概述
建造者模式提供了灵活的方式来构造复杂的塔配置，特别适用于升级系统。

### 文件
- **tower_defence/towers/tower_builder.py**: 定义了塔构造器和预定义配置

### 核心类

#### TowerBuilder
流式API构造塔

```python
from tower_defence.towers.tower_builder import TowerBuilder

# 使用流式API构造塔
tower = (TowerBuilder('basic')
    .at_position(100, 100)
    .with_level(3)
    .with_damage(50)
    .with_range(150)
    .build())
```

#### TowerConfiguration
预定义的塔配置

```python
from tower_defence.towers.tower_builder import TowerConfiguration

# 使用预定义配置
basic = TowerConfiguration.basic_tower(100, 100)
cannon = TowerConfiguration.cannon_tower(200, 100)
sniper = TowerConfiguration.sniper_tower(300, 100)
```

### 用法示例

#### 1. 基础塔
```python
tower = (TowerBuilder('basic')
    .at_position(100, 100)
    .build())
```

#### 2. 升级的塔
```python
tower = (TowerBuilder('basic')
    .at_position(100, 100)
    .with_level(3)
    .build())
```

#### 3. 自定义配置
```python
tower = (TowerBuilder('sniper')
    .at_position(200, 200)
    .with_level(2)
    .with_damage(80)
    .with_range(250)
    .build())
```

#### 4. 快速配置
```python
# 使用预定义配置
cannon = TowerConfiguration.cannon_tower(300, 300)
```

### TowerUpgradeBuilder
用于处理塔升级

```python
from tower_defence.towers.tower_builder import TowerUpgradeBuilder

tower = Tower(100, 100, 'basic')

# 升级塔
upgrade = TowerUpgradeBuilder(tower)
upgrade.upgrade_levels(2).add_damage_bonus(20).apply()
```

### 优势
- ✅ 清晰的代码结构
- ✅ 链式调用易读
- ✅ 灵活的配置选项
- ✅ 易于创建复杂的塔配置
- ✅ 便于进行单位测试

---

## 集成示例

### 在游戏中使用所有模式

```python
from tower_defence.app.game import Game
from tower_defence.combat.attack_strategy import StrongestEnemyStrategy
from tower_defence.towers.tower_builder import TowerBuilder
from tower_defence.systems.event_system import GameEvent, GameEventObserver

# 创建游戏
game = Game()

# 设置事件观察者
observer = GameEventObserver("Game")
game.event_manager.subscribe(GameEvent.TOWER_PLACED, observer)
game.event_manager.subscribe(GameEvent.ENEMY_KILLED, observer)

# 使用构造器模式创建塔
tower = (TowerBuilder('sniper')
    .at_position(150, 150)
    .with_level(2)
    .build())

# 使用策略模式改变攻击策略
tower.set_attack_strategy(StrongestEnemyStrategy())

# 添加塔到游戏
game.towers.append(tower)

# 游戏会自动管理塔的状态（状态模式）
# 并发射适当的事件（观察者模式）
game.update()
```

---

## 最佳实践

### 1. 选择正确的策略
- 基础塔：`ClosestEnemyStrategy` (最近的敌人)
- 快速塔：`FastestEnemyStrategy` (最快的敌人)
- 狙击塔：`StrongestEnemyStrategy` (最强的敌人)
- 防御塔：`FarthestEnemyStrategy` (最先进的敌人)

### 2. 使用事件驱动架构
- 订阅重要事件以更新UI
- 记录事件用于调试
- 使用事件处理复杂的游戏逻辑

### 3. 使用建造者进行复杂配置
- 升级塔时使用`TowerUpgradeBuilder`
- 创建特殊配置的塔时使用`TowerBuilder`
- 使用`TowerConfiguration`获取标准配置

### 4. 正确管理状态转换
- 使用`set_state()`改变塔状态
- 塔会自动处理状态间的转换
- 升级后塔自动转换到`UpgradedState`

---

## 扩展指南

### 添加新的攻击策略
```python
# 在 tower_defence/combat/attack_strategy.py 中
class CustomStrategy(AttackStrategy):
    def get_target(self, tower, enemies):
        # 实现自定义逻辑
        pass
    
    def attack(self, tower, enemies):
        # 实现自定义攻击
        pass
```

### 添加新的塔状态
```python
# 在 tower_defence/towers/tower_state.py 中
class CustomState(TowerState):
    def enter(self, tower):
        pass
    
    def exit(self, tower):
        pass
    
    def handle_attack(self, tower, enemies):
        pass
    
    def get_state_name(self):
        return "Custom"
```

### 添加新的游戏事件
```python
# 在 tower_defence/systems/event_system.py 中的 GameEvent
class GameEvent(Enum):
    # ... 现有事件 ...
    CUSTOM_EVENT = "custom_event"
```

---

## 总结

这些设计模式使塔防游戏代码更加：
- **可维护**: 清晰的结构和责任划分
- **可扩展**: 易于添加新的功能而不修改现有代码
- **可测试**: 独立的组件便于单元测试
- **易读**: 明确的意图和行为

通过结合这四个设计模式，游戏具有高度的灵活性和可维护性，使其易于扩展和改进。
