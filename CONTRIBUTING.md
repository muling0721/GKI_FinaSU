# 贡献指南

## 提交信息规范（Commit Convention）

本仓库的提交信息遵循 [Conventional Commits](https://www.conventionalcommits.org/)，
风格与上游 [LingLuo17/AnyKernel3](https://github.com/LingLuo17/AnyKernel3) 保持一致。

### 格式

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

- `type` / `scope`：小写英文
- `subject`：小写英文、**祈使句**（如 `add` / `fix`，而非 `added` / `fixes`）、**不加句号**、建议 ≤ 72 字符
- 冒号后空一格

### type

| type | 用途 |
|------|------|
| `feat` | 新功能 / 新能力 |
| `fix` | 修复缺陷或构建失败 |
| `refactor` | 重构，不改变外部行为 |
| `docs` | 文档 |
| `chore` | 杂项（数据更新、清理死代码、依赖等） |
| `ci` | CI / 工作流配置 |

### scope（按影响面，可省略）

| scope | 范围 |
|-------|------|
| `ci` | GitHub Actions 工作流、构建流水线 |
| `ksu` | KernelSU 通用集成 |
| `finasu` | FinaSU 相关（SUSFS 集成、preinit、品牌名等） |
| `susfs` | SUSFS 内核补丁与适配 |
| `sukisu` / `bakasu` | 对应变体的兼容代码 |
| `net` | 网络增强（BBRv3 / IPSet / tcp 等） |
| `ntsync` | NTSync 补丁 |
| `ksu-uapi-sync` | UAPI 同步脚本 |
| `release` | 发布流程 |
| `workflow` | 工作流输入 / 交互定义 |

### 示例

```
feat(finasu): brand the kernel full version string as MuLing
fix(susfs): repair trace/hooks context for 5.15 susfs_def.h hunks
fix(ci): use the manager version for AK3 package names
ci: add the 5.10.43 and 5.15.41 builds
docs: add commit message convention
chore: update GKI kernel version data
```

### 反例

```
update                  # 缺 type，信息量不足
Fix Bug.                # 大写、无 scope、带句号、非祈使句
修改了一些东西            # 无法定位影响面
feat: 增加功能            # 过于笼统（除非确实没有合适的 scope）
```

### body（可选）

用于解释 **为什么** 改、影响范围与注意事项。语言不限（中/英文均可），建议用列表：

```
fix(susfs): handle BBRv3 patch context drift on LTS

上游 BBRv3 补丁在 LTS 分支上下文变化，导致 hunk 被拒；
这里按内容探测补回，避免构建失败。
```

### 自动化提交

由 bot 生成的数据更新固定使用：

```
chore: update GKI kernel version data
```

### 合并 / 同步提交

同步上游时保留 Git 默认的 merge 信息（如
`Merge remote-tracking branch 'upstream/main' into dev`），不手工改写。
