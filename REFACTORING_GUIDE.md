# 塔防遊戲 - 設計模式重構

这是对塔防游戏的全面重构，应用了四个主要的设计模式来改进代码的可维护性、可扩展性和灵活性。

## 🎯 项目概述

塔防游戏是一个策略类游戏，玩家放置防御塔来对抗敌人波次。通过应用设计模式，我们使代码更加模块化和可维护。

## 🏗️ 应用的设计模式

### 1. 📊 **策略模式 (Strategy Pattern)**

不同的塔使用不同的攻击策略来选择目标。

**文件**: `tower_defence/combat/attack_strategy.py`

**实现的策略**:
- `ClosestEnemyStrategy` - 攻击最接近的敌人
- `FastestEnemyStrategy` - 攻击最快的敌人
- `StrongestEnemyStrategy` - 攻击血量最多的敌人
- `FarthestEnemyStrategy` - 攻击路径上最先进的敌人

**使用示例**:
```python
tower = Tower(100, 100, 'basic')
tower.set_attack_strategy(StrongestEnemyStrategy())
```

### 2. 🔄 **状态模式 (State Pattern)**

塔可以处于不同的状态，每个状态有不同的行为。

**文件**: `tower_defence/towers/tower_state.py`

**实现的状态**:
- `IdleState` - 闲置状态（搜索目标）
- `AttackingState` - 攻击状态（主动射击）
- `UpgradedState` - 升级状态（增强属性）
- `CooldownState` - 冷却状态（暂时无法射击）

**使用示例**:
```python
tower = Tower(100, 100, 'basic')
tower.upgrade()  # 自动转换到 UpgradedState
```

### 3. 👁️ **观察者模式 (Observer Pattern)**

实现事件驱动架构，游戏组件可以对重要事件做出反应。

**文件**: `tower_defence/systems/event_system.py`

**支持的事件**:
- `ENEMY_SPAWNED` - 敌人生成
- `ENEMY_KILLED` - 敌人被击杀
- `ENEMY_ESCAPED` - 敌人逃脱
- `TOWER_PLACED` - 塔被放置
- `TOWER_UPGRADED` - 塔被升级
- `TOWER_SOLD` - 塔被售出
- `WAVE_STARTED` - 波次开始
- `WAVE_COMPLETED` - 波次完成
- `GAME_OVER` - 游戏结束
- `MONEY_CHANGED` - 金钱变化
- `LIVES_CHANGED` - 生命值变化

**使用示例**:
```python
from tower_defence.systems.event_system import EventManager, GameEvent

event_manager = EventManager()

def on_money_changed(event, data):
    print(f"Money: ${data['money']}")

event_manager.subscribe_callback(GameEvent.MONEY_CHANGED, on_money_changed)
event_manager.emit(GameEvent.MONEY_CHANGED, {'money': 500})
```

### 4. 🔨 **建造者模式 (Builder Pattern)**

灵活地构造复杂的塔配置，特别适用于升级系统。

**文件**: `tower_defence/towers/tower_builder.py`

**类**:
- `TowerBuilder` - 使用流式API构造塔
- `TowerConfiguration` - 预定义的塔配置
- `TowerUpgradeBuilder` - 处理塔升级

**使用示例**:
```python
from tower_defence.towers.tower_builder import TowerBuilder, TowerConfiguration

# 使用流式API
tower = (TowerBuilder('sniper')
    .at_position(100, 100)
    .with_level(3)
    .with_damage(80)
    .build())

# 使用预定义配置
cannon = TowerConfiguration.cannon_tower(200, 200)
```

## 📁 项目结构

```
JustATowerDefence/
├── 设计模式文件/
│   ├── tower_defence/combat/attack_strategy.py   # 策略模式 - 攻击策略
│   ├── tower_defence/towers/tower_state.py       # 状态模式 - 塔状态
│   ├── tower_defence/systems/event_system.py     # 观察者模式 - 事件系统
│   └── tower_defence/towers/tower_builder.py     # 建造者模式 - 塔构造器
│
├── 重构的核心文件/
│   ├── tower_defence/towers/tower.py        # 整合策略和状态模式
│   ├── tower_defence/entities/enemy.py      # 整合观察者模式
│   └── tower_defence/app/game.py            # 整合所有模式
│
├── 原有文件/
│   ├── main.py                 # 游戏主入口
│   ├── tower_defence/entities/projectile.py # 炮弹
│   ├── tower_defence/core/config.py         # 配置
│   └── test_game.py            # 测试
│
├── 文档/
│   ├── DESIGN_PATTERNS.md      # 详细的设计模式文档
│   ├── README.md               # 原始README
│   └── CODEBASE.md             # 代码库文档
│
└── 示例和验证/
    ├── design_patterns_demo.py # 设计模式演示
    └── validate_patterns.py    # 设计模式验证脚本
```

## 🚀 快速开始

### 安装依赖
```bash
pip install pygame
```

### 运行游戏
```bash
python3 main.py
```

### 验证设计模式
```bash
python3 validate_patterns.py
```

### 查看设计模式演示
要运行完整演示，需要将 `design_patterns_demo.py` 中的 pygame 导入改为可选：

```bash
# 当 pygame 安装时
python3 design_patterns_demo.py

# 或查看演示代码（需要 pygame）
python3 -c "from design_patterns_demo import run_all_demos; run_all_demos()"
```

## 📚 文档

- **[DESIGN_PATTERNS.md](DESIGN_PATTERNS.md)** - 详细的设计模式说明和用法示例
- **[CODEBASE.md](docs/CODEBASE.md)** - 原始代码库文档

## 🔑 关键改进

### 可维护性
✅ 清晰的代码结构  
✅ 职责分离  
✅ 易于理解的流程  

### 可扩展性
✅ 轻松添加新策略  
✅ 轻松添加新状态  
✅ 轻松添加新事件  
✅ 轻松创建新塔配置  

### 灵活性
✅ 运行时改变塔的攻击策略  
✅ 动态管理塔的状态  
✅ 事件驱动架构  
✅ 灵活的塔配置系统  

### 可测试性
✅ 独立的组件便于单元测试  
✅ 事件系统便于模拟和验证  
✅ 没有紧耦合  

## 💡 使用示例

### 示例 1: 创建具有特定策略的塔

```python
from tower_defence.app.game import Game
from tower_defence.combat.attack_strategy import StrongestEnemyStrategy
from tower_defence.towers.tower import Tower

game = Game()

# 创建塔
tower = Tower(100, 100, 'sniper')

# 设置攻击最强的敌人
tower.set_attack_strategy(StrongestEnemyStrategy())

# 添加到游戏
game.towers.append(tower)
```

### 示例 2: 使用事件系统

```python
from tower_defence.systems.event_system import EventManager, GameEvent, GameEventObserver

# 创建事件管理器
events = EventManager()

# 创建观察者
observer = GameEventObserver("Logger")

# 订阅事件
events.subscribe(GameEvent.TOWER_PLACED, observer)
events.subscribe(GameEvent.ENEMY_KILLED, observer)

# 发射事件
events.emit(GameEvent.TOWER_PLACED, {
    'position': (100, 100),
    'type': 'basic'
})
```

### 示例 3: 使用构造器创建塔

```python
from tower_defence.towers.tower_builder import TowerBuilder, TowerConfiguration

# 使用流式API
tower1 = (TowerBuilder('basic')
    .at_position(100, 100)
    .with_level(2)
    .with_damage(50)
    .build())

# 使用预定义配置
tower2 = TowerConfiguration.sniper_tower(200, 200)

# 创建完全自定义的塔
tower3 = (TowerBuilder('cannon')
    .at_position(300, 300)
    .with_level(3)
    .with_damage(80)
    .with_range(200)
    .with_aoe(60)
    .build())
```

### 示例 4: 改变塔的状态

```python
from tower_defence.towers.tower import Tower
from tower_defence.towers.tower_state import AttackingState, CooldownState

tower = Tower(100, 100, 'basic')

# 改变到攻击状态
tower.set_state(AttackingState())

# 改变到冷却状态
tower.set_state(CooldownState(cooldown_frames=20))
```

## 🎮 游戏流程

1. **初始化**: 创建 `Game` 实例
2. **事件设置**: 订阅重要事件
3. **波次管理**: 调用 `start_wave()` 开始敌人波次
4. **塔部署**: 使用 `add_tower()` 放置塔
5. **游戏循环**: 调用 `update()` 更新游戏状态
6. **事件处理**: 观察者响应游戏事件
7. **游戏结束**: 当 `game_over` 为 True 时结束

## 🔄 集成流程

所有设计模式在游戏中无缝集成：

```
Game 类
├── 使用 TowerBuilder (建造者模式) 创建塔
├── 设置塔的 AttackStrategy (策略模式)
├── 管理塔的 State (状态模式)
├── 发射 GameEvent (观察者模式)
│
Tower 类
├── 维护 AttackStrategy
├── 维护 TowerState
└── 发射事件
│
Enemy 类
├── 发射被击杀事件
└── 发射逃脱事件
│
EventManager
├── 管理所有事件
└── 通知观察者
```

## 📊 性能特性

- **内存效率**: 最小化对象创建
- **计算效率**: 仅更新活跃的实体
- **事件优化**: 事件过滤避免不必要的处理

## 🐛 调试

### 启用日志记录
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 验证模式
```bash
python3 validate_patterns.py
```

## 🤝 贡献

当添加新功能时：
1. 遵循现有的设计模式
2. 确保新代码与既有模式兼容
3. 为新的策略/状态/事件添加相应的类
4. 更新 DESIGN_PATTERNS.md 文档

## 📄 许可证

见 [LICENSE](LICENSE) 文件

## 🙏 致谢

这个重构展示了如何使用设计模式来改进游戏代码的质量和可维护性。

---

**最后更新**: 2026年2月28日  
**设计模式版本**: 1.0

如有问题，请参考 [DESIGN_PATTERNS.md](DESIGN_PATTERNS.md) 获取详细信息。
