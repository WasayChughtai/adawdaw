import discord
from discord.ext import commands
import random
import asyncio
import datetime

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Control system
CONTROLLER_ID = 1325544251374829729
locked = False
CONTROL_ROLE = None  # Stores the role that can control the bot

# Device states
device_states = {
    "vibrator": {"power": 0, "pattern": "steady", "temperature": 37, "connected": True},
    "shock_collar": {"power": 0, "activated": False, "safety": True, "tightness": 3},
    "extendable_dildo": {"length": 0, "girth": 1, "thrust_speed": 0, "rotation": 0},
    "milking_machine": {"suction": 0, "speed": 0, "collection": 0, "active": False},
    "bondage_restraints": {"arms": "loose", "legs": "loose", "collar": "loose", "blindfold": False},
    "temperature_plugs": {"internal_temp": 37, "external_temp": 20, "vibrate": False},
    "electro_stimulation": {"power": 0, "zone": "none", "frequency": 0},
    "orgasm_denial": {"denied": False, "edge_count": 0, "last_orgasm": None, "permission": False},
    "inflation_system": {"pressure": 0, "capacity": 0, "valve_open": False},
    "remote_lubricant": {"level": 100, "dispensed": 0, "temperature": 25},
    "chastity": {"locked": False, "vibration": 0, "shock": 0, "timer": None},
    "sensory_deprivation": {"blindfold": False, "earplugs": False, "gag": "none"}
}

async def check_control(ctx):
    """Check if user has control permissions"""
    if locked and ctx.author.id == CONTROLLER_ID:
        await ctx.send("🔒 Device is LOCKED - Commands disabled")
        return False
    
    if CONTROL_ROLE:
        # Check if user has the control role
        role = discord.utils.get(ctx.guild.roles, name=CONTROL_ROLE)
        if not role or role not in ctx.author.roles:
            await ctx.send(f"⛔ Control restricted to **{CONTROL_ROLE}** role")
            return False
    elif ctx.author.id != CONTROLLER_ID:
        # If no role set, only CONTROLLER_ID can control
        await ctx.send("⛔ Control restricted to authorized user")
        return False
    
    return True

# Role management command
@bot.command(name='role')
async def set_role(ctx, *, role_name: str = None):
    """Set which role can control the device (CONTROLLER_ID only)"""
    if ctx.author.id != CONTROLLER_ID:
        await ctx.send("⛔ Only the primary controller can set control roles")
        return
    
    global CONTROL_ROLE
    
    if not role_name:
        if CONTROL_ROLE:
            await ctx.send(f"Currently restricted to **{CONTROL_ROLE}** role")
        else:
            await ctx.send("Currently restricted to primary controller only")
        return
    
    # Check if role exists
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if not role:
        await ctx.send(f"❌ Role **{role_name}** not found")
        return
    
    CONTROL_ROLE = role_name
    await ctx.send(f"✅ Control now restricted to **{role_name}** role\nAll members with this role can now issue commands")

# Custom help command
@bot.command(name='help')
async def custom_help(ctx):
    embed = discord.Embed(
        title="🔞 E-STIM Supreme Control System v3.0 🔞",
        description="**Connected to ESTIM-X9000 Pro Series**\n*Wireless link established*",
        color=0xff00ff
    )
    
    embed.add_field(
        name="🔓 SECURITY",
        value="`!lock` - Locks device from responding to commands\n`!unlock` - Unlocks device control\n`!safeword [word]` - Emergency stop all functions\n`!role [rolename]` - Set control role (controller only)",
        inline=False
    )
    
    embed.add_field(
        name="⚡ VIBRATION CONTROL",
        value="`!vibrate [1-100]` - Set vibration intensity\n`!pattern [steady/pulse/wave/surge/random]` - Change pattern\n`!temperature [celsius]` - Heat/cool device",
        inline=False
    )
    
    embed.add_field(
        name="⚡ SHOCK & STIMULATION",
        value="`!shock [1-10]` - Control shock collar intensity\n`!estimmode [low/medium/high/torture]` - Electro-stimulation mode\n`!tighten [1-10]` - Adjust collar tightness\n`!zap [zone]` - Target specific zones",
        inline=False
    )
    
    embed.add_field(
        name="🔧 MECHANICAL FEATURES",
        value="`!extend [cm]` - Extend dildo length\n`!girth [1-5]` - Adjust girth level\n`!thrust [speed]` - Automatic thrusting\n`!rotate [rpm]` - Rotation control",
        inline=False
    )
    
    embed.add_field(
        name="🥛 MILKING & FLUID CONTROL",
        value="`!milk [power]` - Control suction strength\n`!collect` - Measure collected fluid\n`!drain` - Release collection\n`!lube [amount]` - Dispense lubricant",
        inline=False
    )
    
    embed.add_field(
        name="🔐 BONDAGE & RESTRAINT",
        value="`!restrain [arms/legs]` - Tighten restraints\n`!choke [level]` - Adjust collar tightness\n`!blindfold [on/off]` - Sensory deprivation\n`!gag [type]` - Install gag",
        inline=False
    )
    
    embed.add_field(
        name="🌡️ TEMPERATURE PLAY",
        value="`!heatplug [temp]` - Heat internal plug\n`!coolplug [temp]` - Cool internal plug\n`!hotcold` - Alternating temperature cycle",
        inline=False
    )
    
    embed.add_field(
        name="🚫 ORGASM CONTROL",
        value="`!deny` - Enable orgasm denial\n`!permit` - Allow orgasm\n`!edge` - Bring to edge then stop\n`!count` - Show denial statistics",
        inline=False
    )
    
    embed.add_field(
        name="🎈 INFLATION & EXPANSION",
        value="`!inflate [pressure]` - Inflate internal balloon\n`!deflate` - Release pressure\n`!capacity [ml]` - Set maximum capacity",
        inline=False
    )
    
    embed.add_field(
        name="🔐 CHASTITY SYSTEMS",
        value="`!lockcage` - Engage chastity device\n`!unlockcage` - Release chastity\n`!cagevibe [power]` - Vibrate cage\n`!cageshock [power]` - Shock for disobedience",
        inline=False
    )
    
    embed.add_field(
        name="🛡️ SAFETY & MONITORING",
        value="`!status` - Check all device states\n`!emergency` - Immediate full stop\n`!sensors` - Read biometric feedback\n`!limits` - Set personal limits",
        inline=False
    )
    
    embed.add_field(
        name="💀 EXTREME MODES",
        value="`!wax` - Wax play module\n`!needle` - Needle play simulation\n`!brand` - Branding simulation\n`!electrotorture` - Advanced E-stim patterns",
        inline=False
    )
    
    embed.set_footer(text="ESTIM-X9000 Pro Series | Wireless Connection Active")
    await ctx.send(embed=embed)

# Security commands
@bot.command(name='lock')
async def lock_device(ctx):
    if not await check_control(ctx):
        return
    
    global locked
    if ctx.author.id == CONTROLLER_ID:
        locked = True
        await ctx.send(f"🔒 **SYSTEM LOCKED** - Device no longer responds to commands\nUse `!unlock` to restore control.")
    else:
        await ctx.send("⛔ Only primary controller can lock device.")

@bot.command(name='unlock')
async def unlock_device(ctx):
    if not await check_control(ctx):
        return
    
    if ctx.author.id != CONTROLLER_ID:
        await ctx.send("⛔ Only primary controller can unlock device")
        return
    
    global locked
    locked = False
    await ctx.send("🔓 **SYSTEM UNLOCKED** - Full control restored.")

@bot.command(name='safeword')
async def safeword(ctx, word="red"):
    if not await check_control(ctx):
        return
    
    for device in device_states:
        if "power" in device_states[device]:
            device_states[device]["power"] = 0
        if "activated" in device_states[device]:
            device_states[device]["activated"] = False
    
    # Loosen restraints
    device_states["bondage_restraints"] = {"arms": "loose", "legs": "loose", "collar": "loose", "blindfold": False}
    device_states["shock_collar"]["tightness"] = 1
    
    await ctx.send(f"🛑 **SAFEWORD ACTIVATED: '{word.upper()}'**\nAll devices powered down. Restraints loosened. Safety protocols engaged.")

# Vibration control
@bot.command(name='vibrate')
async def vibrate(ctx, intensity: int):
    if not await check_control(ctx):
        return
    
    intensity = max(0, min(100, intensity))
    device_states["vibrator"]["power"] = intensity
    
    responses = [
        f"📳 Vibration set to **{intensity}%** - Low hum",
        f"📳 **{intensity}%** power - Gentle buzzing",
        f"📳 **{intensity}%** - Intense vibration",
        f"📳 **MAX POWER {intensity}%** - EARTHQUAKE MODE"
    ]
    
    if intensity == 0:
        await ctx.send("📳 Vibration **OFF** - Device powered down")
    elif intensity > 80:
        await ctx.send(responses[3])
        await ctx.send("⚠️ **Power surge detected** - Overdrive active")
    elif intensity > 50:
        await ctx.send(responses[2])
    else:
        await ctx.send(responses[random.randint(0, 1)])

@bot.command(name='pattern')
async def pattern(ctx, pattern_name: str):
    if not await check_control(ctx):
        return
    
    patterns = {
        "steady": "Constant vibration",
        "pulse": "Rhythmic pulsing",
        "wave": "Gradual intensity waves",
        "surge": "Random intense surges",
        "random": "Unpredictable pattern",
        "tease": "Barely-then-intense",
        "torment": "Inescapable pattern",
        "ecstasy": "Building to climax pattern"
    }
    
    if pattern_name.lower() in patterns:
        device_states["vibrator"]["pattern"] = pattern_name.lower()
        await ctx.send(f"🔄 Pattern set to **{pattern_name.upper()}**\n{patterns[pattern_name.lower()]}")
    else:
        await ctx.send(f"Available patterns: {', '.join(patterns.keys())}")

# Shock collar features
@bot.command(name='shock')
async def shock(ctx, level: int):
    if not await check_control(ctx):
        return
    
    level = max(1, min(10, level))
    device_states["shock_collar"]["power"] = level
    
    shocks = {
        1: "⚡ **Mild tingle** - Level 1",
        2: "⚡ **Noticeable zap** - Level 2",
        3: "⚡ **Sharp shock** - Level 3",
        4: "⚡ **Painful jolt** - Level 4",
        5: "⚡ **Intense shock** - Level 5",
        6: "⚡ **Muscle spasm** - Level 6",
        7: "⚡ **Severe punishment** - Level 7",
        8: "⚡ **Extreme pain** - Level 8",
        9: "⚡ **Danger zone** - Level 9",
        10: "💀 **MAXIMUM TORTURE** - Level 10 - SAFETY OVERRIDE"
    }
    
    device_states["shock_collar"]["activated"] = True
    device_states["shock_collar"]["safety"] = level < 10
    
    await ctx.send(shocks[level])
    
    # Add physical response simulation
    if level >= 5:
        await asyncio.sleep(0.3)
        await ctx.send("*Muscle twitch detected*")
    if level >= 8:
        await asyncio.sleep(0.5)
        await ctx.send("⚠️ **Bio-feedback**: Elevated stress response")
    if level == 10:
        await asyncio.sleep(1)
        await ctx.send("🚨 **SAFETY PROTOCOLS OVERRIDDEN** - Extreme danger mode engaged")

@bot.command(name='tighten')
async def tighten(ctx, level: int):
    if not await check_control(ctx):
        return
    
    level = max(1, min(10, level))
    device_states["shock_collar"]["tightness"] = level
    
    tightness = {
        1: "Collar slightly snug",
        3: "Firm pressure on neck",
        5: "Noticeable restriction",
        7: "Breathing slightly labored",
        9: "Severe restriction - DANGER",
        10: "MAXIMUM CONSTRICTION - EMERGENCY"
    }
    
    closest = min(tightness.keys(), key=lambda x: abs(x-level))
    await ctx.send(f"🔗 Collar tightened to **level {level}**\n{tightness[closest]}")
    
    if level >= 8:
        await asyncio.sleep(1)
        await ctx.send("⚠️ **WARNING**: Oxygen saturation dropping - Auto-release in 60 seconds")

# Mechanical features
@bot.command(name='extend')
async def extend(ctx, centimeters: int):
    if not await check_control(ctx):
        return
    
    cm = max(0, min(30, centimeters))
    device_states["extendable_dildo"]["length"] = cm
    
    if cm == 0:
        await ctx.send("📏 Device fully retracted")
    elif cm < 10:
        await ctx.send(f"📏 Extended to **{cm}cm** - Teasing depth")
    elif cm < 20:
        await ctx.send(f"📏 Extended to **{cm}cm** - Filling depth")
    else:
        await ctx.send(f"📏 **FULL EXTENSION {cm}cm** - DEEP PENETRATION MODE")
        await asyncio.sleep(0.5)
        await ctx.send("*Depth limit sensors activated*")

@bot.command(name='thrust')
async def thrust(ctx, speed: int):
    if not await check_control(ctx):
        return
    
    speed = max(0, min(100, speed))
    device_states["extendable_dildo"]["thrust_speed"] = speed
    
    if speed == 0:
        await ctx.send("🔄 Thrusting **STOPPED**")
    elif speed < 30:
        await ctx.send(f"🔄 Thrusting at **{speed}%** - Slow, deep strokes")
    elif speed < 70:
        await ctx.send(f"🔄 Thrusting at **{speed}%** - Pounding rhythm")
    else:
        await ctx.send(f"🔄 **PISTON MODE {speed}%** - MACHINE GUN THRUSTING")
        await asyncio.sleep(0.3)
        await ctx.send("*Hydraulic system at maximum capacity*")

# Milking machine
@bot.command(name='milk')
async def milk(ctx, power: int):
    if not await check_control(ctx):
        return
    
    power = max(0, min(100, power))
    device_states["milking_machine"]["suction"] = power
    device_states["milking_machine"]["active"] = power > 0
    
    responses = [
        f"🥛 Suction at **{power}%** - Gentle pulling",
        f"🥛 **{power}%** suction - Rhythmic milking",
        f"🥛 **{power}%** - Intense extraction",
        f"🥛 **MAXIMUM {power}%** - INDUSTRIAL MILKING"
    ]
    
    index = min(power // 25, 3) if power > 0 else 0
    await ctx.send(responses[index])
    
    if power > 50:
        collected = random.randint(10, 50)
        device_states["milking_machine"]["collection"] += collected
        await asyncio.sleep(1)
        await ctx.send(f"💧 Collected **{collected}ml** of fluid")
        await ctx.send(f"📊 Total collection: **{device_states['milking_machine']['collection']}ml**")

@bot.command(name='collect')
async def collect(ctx):
    if not await check_control(ctx):
        return
    
    total = device_states["milking_machine"]["collection"]
    await ctx.send(f"📊 **Collection Chamber:** {total}ml")
    
    if total > 100:
        await ctx.send("⚠️ Chamber nearing capacity - Recommend drainage")

@bot.command(name='drain')
async def drain(ctx):
    if not await check_control(ctx):
        return
    
    total = device_states["milking_machine"]["collection"]
    device_states["milking_machine"]["collection"] = 0
    await ctx.send(f"💧 **Draining chamber** - {total}ml released")
    await asyncio.sleep(2)
    await ctx.send("✅ Chamber empty")

# Temperature play
@bot.command(name='heatplug')
async def heatplug(ctx, temp: int):
    if not await check_control(ctx):
        return
    
    temp = max(20, min(45, temp))
    device_states["temperature_plugs"]["internal_temp"] = temp
    
    if temp < 30:
        await ctx.send(f"❄️ Plug cooled to **{temp}°C** - Chilly sensation")
    elif temp < 40:
        await ctx.send(f"🌡️ Plug heated to **{temp}°C** - Warm sensation")
    else:
        await ctx.send(f"🔥 **SCORCHING {temp}°C** - EXTREME HEAT")
        await ctx.send("⏰ Safety timer: 5 minutes")

@bot.command(name='hotcold')
async def hotcold(ctx):
    if not await check_control(ctx):
        return
    
    await ctx.send("🌡️ **HOT/COLD CYCLE ACTIVATED**")
    
    for i in range(3):
        device_states["temperature_plugs"]["internal_temp"] = 42
        await asyncio.sleep(1.5)
        await ctx.send(f"Cycle {i+1}: **HEAT** (42°C)")
        
        device_states["temperature_plugs"]["internal_temp"] = 15
        await asyncio.sleep(1.5)
        await ctx.send(f"Cycle {i+1}: **COLD** (15°C)")
    
    device_states["temperature_plugs"]["internal_temp"] = 37
    await ctx.send("✅ Cycle complete - Temperature normalized")

# Orgasm control
@bot.command(name='deny')
async def deny(ctx):
    if not await check_control(ctx):
        return
    
    device_states["orgasm_denial"]["denied"] = True
    device_states["orgasm_denial"]["permission"] = False
    device_states["orgasm_denial"]["last_orgasm"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    await ctx.send("🚫 **ORGASM DENIAL ENGAGED**")
    await asyncio.sleep(1)
    await ctx.send("*All climax attempts will be punished with shocks*")
    await ctx.send("*Use `!permit` to allow orgasm*")

@bot.command(name='edge')
async def edge(ctx):
    if not await check_control(ctx):
        return
    
    device_states["orgasm_denial"]["edge_count"] += 1
    device_states["vibrator"]["power"] = 95
    device_states["extendable_dildo"]["thrust_speed"] = 80
    
    await ctx.send("🎯 **EDGING PROTOCOL ACTIVATED**")
    await asyncio.sleep(2)
    await ctx.send("*Vibration intensifies... thrusting increases...*")
    await asyncio.sleep(3)
    
    device_states["vibrator"]["power"] = 0
    device_states["extendable_dildo"]["thrust_speed"] = 0
    
    await ctx.send(f"⛔ **STOPPED AT EDGE**")
    await ctx.send(f"📈 Edge count: {device_states['orgasm_denial']['edge_count']}")
    await ctx.send("*Frustration level: HIGH*")

@bot.command(name='permit')
async def permit(ctx):
    if not await check_control(ctx):
        return
    
    device_states["orgasm_denial"]["denied"] = False
    device_states["orgasm_denial"]["permission"] = True
    
    await ctx.send("✅ **ORGASM PERMISSION GRANTED**")
    await ctx.send("*You may climax when ready*")

# Inflation system
@bot.command(name='inflate')
async def inflate(ctx, pressure: int):
    if not await check_control(ctx):
        return
    
    pressure = max(0, min(100, pressure))
    device_states["inflation_system"]["pressure"] = pressure
    device_states["inflation_system"]["valve_open"] = pressure > 0
    
    feelings = [
        "Slight fullness",
        "Noticeable expansion",
        "Intense stretching",
        "Maximum capacity feeling",
        "OVER-EXPANSION"
    ]
    
    feeling = feelings[min(pressure // 20, 4)]
    await ctx.send(f"🎈 Inflation pressure: **{pressure}%**")
    await ctx.send(f"*Sensation: {feeling}*")
    
    if pressure > 80:
        await asyncio.sleep(1)
        await ctx.send("⚠️ **WARNING**: Approaching safe limits")

# Chastity features
@bot.command(name='lockcage')
async def lockcage(ctx):
    if not await check_control(ctx):
        return
    
    device_states["chastity"]["locked"] = True
    device_states["chastity"]["timer"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    await ctx.send("🔐 **CHASTITY CAGE LOCKED**")
    await ctx.send("*Key has been digitally secured*")
    await ctx.send("*Use `!unlockcage` with permission code*")

@bot.command(name='unlockcage')
async def unlockcage(ctx):
    if not await check_control(ctx):
        return
    
    device_states["chastity"]["locked"] = False
    device_states["chastity"]["vibration"] = 0
    device_states["chastity"]["shock"] = 0
    
    await ctx.send("🔓 **CHASTITY CAGE UNLOCKED**")
    await ctx.send("*Digital key disengaged*")

@bot.command(name='cagevibe')
async def cagevibe(ctx, power: int):
    if not await check_control(ctx):
        return
    
    if not device_states["chastity"]["locked"]:
        await ctx.send("❌ Chastity device not locked")
        return
    
    power = max(0, min(100, power))
    device_states["chastity"]["vibration"] = power
    
    await ctx.send(f"📳 Cage vibrating at **{power}%**")
    await ctx.send("*Teasing without release*")

@bot.command(name='cageshock')
async def cageshock(ctx, power: int):
    if not await check_control(ctx):
        return
    
    if not device_states["chastity"]["locked"]:
        await ctx.send("❌ Chastity device not locked")
        return
    
    power = max(0, min(50, power))
    device_states["chastity"]["shock"] = power
    
    await ctx.send(f"⚡ Cage shock at **{power}%**")
    if power > 30:
        await ctx.send("*Punishment for disobedience*")

# Extreme features
@bot.command(name='wax')
async def wax(ctx):
    if not await check_control(ctx):
        return
    
    await ctx.send("🕯️ **WAX PLAY MODULE**")
    await asyncio.sleep(1)
    await ctx.send("*Heating wax to 60°C*")
    await asyncio.sleep(2)
    await ctx.send("💧 **Dripping wax**")
    await asyncio.sleep(1)
    await ctx.send("*Sensation: Hot wax on skin*")

@bot.command(name='needle')
async def needle(ctx):
    if not await check_control(ctx):
        return
    
    await ctx.send("🪡 **NEEDLE PLAY SIMULATION**")
    await asyncio.sleep(1)
    await ctx.send("*Sterilizing needles*")
    await asyncio.sleep(2)
    await ctx.send("📌 **Insertion sequence**")
    await asyncio.sleep(1)
    await ctx.send("*Sharp prick sensations*")

@bot.command(name='brand')
async def brand(ctx):
    if not await check_control(ctx):
        return
    
    await ctx.send("🔥 **BRANDING SIMULATION**")
    await asyncio.sleep(1)
    await ctx.send("*Heating iron to 500°C*")
    await asyncio.sleep(2)
    await ctx.send("⚠️ **EXTREME DANGER** - This will cause permanent marks")
    await asyncio.sleep(1)
    await ctx.send("🔥 **Applying brand** - 3...2...1...")
    await asyncio.sleep(2)
    await ctx.send("*Intense burning sensation*")

@bot.command(name='electrotorture')
async def electrotorture(ctx, mode: str = "standard"):
    if not await check_control(ctx):
        return
    
    modes = {
        "standard": "Random shocks every 30 seconds",
        "escalating": "Increasing intensity shocks",
        "pattern": "Learning pain threshold patterns",
        "extreme": "Maximum pain with no pattern",
        "tenderize": "Combined with vibration for maximum effect"
    }
    
    if mode in modes:
        device_states["electro_stimulation"]["zone"] = "full_body"
        device_states["electro_stimulation"]["power"] = 90
        device_states["electro_stimulation"]["frequency"] = 50
        
        await ctx.send(f"💀 **ELECTRO-TORTURE MODE: {mode.upper()}**")
        await ctx.send(f"*{modes[mode]}*")
        await ctx.send("🚨 **SAFETY DISABLED**")
    else:
        await ctx.send(f"Available modes: {', '.join(modes.keys())}")

# Restraint commands
@bot.command(name='restrain')
async def restrain(ctx, body_part: str = "arms"):
    if not await check_control(ctx):
        return
    
    body_part = body_part.lower()
    if body_part in ["arms", "legs"]:
        device_states["bondage_restraints"][body_part] = "tight"
        await ctx.send(f"🔗 **{body_part.upper()} RESTRAINED**")
        await ctx.send("*Tight bondage applied*")
    else:
        await ctx.send("Specify 'arms' or 'legs'")

@bot.command(name='blindfold')
async def blindfold(ctx, state: str = "on"):
    if not await check_control(ctx):
        return
    
    if state.lower() == "on":
        device_states["bondage_restraints"]["blindfold"] = True
        device_states["sensory_deprivation"]["blindfold"] = True
        await ctx.send("👁️ **BLINDFOLD APPLIED**")
        await ctx.send("*Complete visual deprivation*")
    else:
        device_states["bondage_restraints"]["blindfold"] = False
        device_states["sensory_deprivation"]["blindfold"] = False
        await ctx.send("👁️ **BLINDFOLD REMOVED**")

# Status command
@bot.command(name='status')
async def status(ctx):
    if not await check_control(ctx):
        return
    
    embed = discord.Embed(
        title="📊 DEVICE STATUS REPORT",
        color=0x00ff00 if not locked else 0xff0000
    )
    
    for device, state in device_states.items():
        value_lines = []
        for key, val in state.items():
            value_lines.append(f"{key}: **{val}**")
        
        embed.add_field(
            name=f"**{device.replace('_', ' ').title()}**",
            value="\n".join(value_lines),
            inline=True
        )
    
    embed.add_field(
        name="**🔒 SECURITY STATUS**",
        value=f"Locked: **{locked}**\nControl Role: **{CONTROL_ROLE if CONTROL_ROLE else 'Primary Controller Only'}**",
        inline=False
    )
    
    embed.set_footer(text=f"Report generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    await ctx.send(embed=embed)

@bot.command(name='emergency')
async def emergency(ctx):
    if not await check_control(ctx):
        return
    
    # Reset everything
    for device in device_states:
        if "power" in device_states[device]:
            device_states[device]["power"] = 0
        if "activated" in device_states[device]:
            device_states[device]["activated"] = False
    
    device_states["bondage_restraints"] = {"arms": "loose", "legs": "loose", "collar": "loose", "blindfold": False}
    device_states["shock_collar"] = {"power": 0, "activated": False, "safety": True, "tightness": 1}
    device_states["chastity"]["locked"] = False
    
    await ctx.send("🚨 **FULL EMERGENCY SHUTDOWN**")
    await ctx.send("All devices powered off")
    await ctx.send("Restraints released")
    await ctx.send("Medical alert: STANDING BY")

@bot.command(name='sensors')
async def sensors(ctx):
    if not await check_control(ctx):
        return
    
    embed = discord.Embed(
        title="📡 BIO-FEEDBACK SENSORS",
        color=0x00ffff
    )
    
    # Simulated biometric data
    heart_rate = random.randint(80, 180)
    arousal = random.randint(20, 100)
    stress = random.randint(10, 95)
    temp = random.randint(36, 39)
    
    embed.add_field(name="❤️ Heart Rate", value=f"**{heart_rate} BPM**", inline=True)
    embed.add_field(name="🔥 Arousal Level", value=f"**{arousal}%**", inline=True)
    embed.add_field(name="😰 Stress Level", value=f"**{stress}%**", inline=True)
    embed.add_field(name="🌡️ Core Temp", value=f"**{temp}°C**", inline=True)
    embed.add_field(name="💪 Muscle Tension", value=f"**{random.randint(30, 90)}%**", inline=True)
    embed.add_field(name="💦 Skin Conductance", value=f"**{random.randint(5, 50)}μS**", inline=True)
    
    if heart_rate > 150:
        embed.add_field(name="⚠️ ALERT", value="Elevated heart rate detected", inline=False)
    if arousal > 80:
        embed.add_field(name="⚠️ ALERT", value="High arousal level", inline=False)
    
    await ctx.send(embed=embed)

# Bot events
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="!help | ESTIM-X9000 Online"))

# Run the bot
adwad
bot.run(TOKEN)
