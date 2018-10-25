#include <iostream>

#include <string>

#include <vector>
#include <array>
#include <set>
#include <map>
#include <queue>

#include <chrono>
#include <algorithm>
#include <memory>

using namespace std;

#pragma region 定数宣言

constexpr int Inf = 999999999;

constexpr char Wall = '#';
constexpr char Spawner = 'w';
constexpr char Shelter = 'U';
constexpr char Empty = '.';

namespace Object {

	const string EXPLORER = "EXPLORER";
	const string WANDERER = "WANDERER";
	const string SLASHER = "SLASHER";
	const string EFFECT_PLAN = "EFFECT_PLAN";
	const string EFFECT_LIGHT = "EFFECT_LIGHT";
	const string EFFECT_SHELTER = "EFFECT_SHELTER";
	const string EFFECT_YELL = "EFFECT_YELL";

	const int SPAWNING = 0;
	const int WANDERING = 1;
	const int STALKING = 2;
	const int RUSHING = 3;
	const int STUNNED = 4;

}

enum class Cell : char
{
	/// <summary>
	/// <para>壁</para>
	/// <para>エンティティは通り抜けできない</para>
	/// </summary>
	Wall,
	/// <summary>
	/// <para>トンべりスポナー</para>
	/// <para>トンべりが出現する</para>
	/// </summary>
	Spawner,
	/// <summary>
	/// <para>シェルター</para>
	/// <para>マス上のプレイヤーを5回復する</para>
	/// <para>10個の回復薬を持っている。回復薬は50ターン枚に10補充される</para>
	/// </summary>
	Shelter,
	/// <summary>
	/// <para>通路</para>
	/// <para>エンティティが通行できる</para>
	/// </summary>
	Empty,
};

#pragma endregion

#pragma region データ構造

struct Point {
	int x;
	int y;

	Point() :Point(-1, -1) {}
	Point(const int _x, const int _y) { x = _x; y = _y; }

	const Point operator+(const Point& p) const { return Point(x + p.x, y + p.y); }
	const Point operator-(const Point& p) const { return Point(x - p.x, y - p.y); }

	const bool operator==(const Point& p) const { return (x == p.x && y == p.y); }
	const bool operator!=(const Point& p) const { return !(*this == p); }

	operator bool() const { return x != -1 && y != -1; }

	const string toString() const { return "(" + to_string(x) + " " + to_string(y) + ")"; }

};

struct Entitie {

	Entitie() : Entitie(-1, Point(), -1, -1, -1) {}
	Entitie(const int _id, const Point& _pos, const int _param0, const int _param1, const int _param2) {
		id = _id;
		pos = _pos;
		param0 = _param0;
		param1 = _param1;
		param2 = _param2;
	}

	int id;
	Point pos;
	int param0;
	int param1;
	int param2;

	int count = 0;
	Point nextPos;
};

using Entities = vector<Entitie>;

#pragma endregion

#pragma region ライブラリ

/// <summary>
/// 時間計測を行うクラス
/// </summary>
class Stopwatch {
public:

	/// <summary>
	/// コンストラクタ
	/// </summary>
	Stopwatch() = default;

	/// <summary>
	/// 計測を開始する
	/// </summary>
	inline void start() {
		s = std::chrono::high_resolution_clock::now();
		e = s;
	}
	/// <summary>
	/// 計測を停止する
	/// </summary>
	inline void stop() {
		e = std::chrono::high_resolution_clock::now();
	}

	/// <summary>
	/// 計測時間を取得する(ナノ秒)
	/// </summary>
	/// <returns>計測時間(ナノ秒)</returns>
	inline const long long nanoseconds() const { return std::chrono::duration_cast<std::chrono::nanoseconds>(e - s).count(); }
	/// <summary>
	/// 計測時間を取得する(マイクロ秒)
	/// </summary>
	/// <returns>計測時間(マイクロ秒)</returns>
	inline const long long microseconds() const { return std::chrono::duration_cast<std::chrono::microseconds>(e - s).count(); }
	/// <summary>
	/// 計測時間を取得する(ミリ秒)
	/// </summary>
	/// <returns>計測時間(ミリ秒)</returns>
	inline const long long millisecond() const { return std::chrono::duration_cast<std::chrono::milliseconds>(e - s).count(); }
	/// <summary>
	/// 計測時間を取得する(秒)
	/// </summary>
	/// <returns>計測時間(秒)</returns>
	inline const long long second() const { return std::chrono::duration_cast<std::chrono::seconds>(e - s).count(); }
	/// <summary>
	/// 計測時間を取得する(分)
	/// </summary>
	/// <returns>計測時間(分)</returns>
	inline const long long minutes() const { return std::chrono::duration_cast<std::chrono::minutes>(e - s).count(); }
	/// <summary>
	/// 計測時間を取得する(時)
	/// </summary>
	/// <returns>計測時間(時)</returns>
	inline const long long hours() const { return std::chrono::duration_cast<std::chrono::hours>(e - s).count(); }

	/// <summary>
	/// 単位付きの計測時間の文字列を得る(ナノ秒)
	/// </summary>
	/// <returns>計測時間の文字列(ナノ秒)</returns>
	inline const std::string toString_ns() const { return std::to_string(nanoseconds()) + "ns"; }
	/// <summary>
	/// 単位付きの計測時間の文字列を得る(マイクロ秒)
	/// </summary>
	/// <returns>計測時間の文字列(マイクロ秒)</returns>
	inline const std::string toString_us() const { return std::to_string(microseconds()) + "us"; }
	/// <summary>
	/// 単位付きの計測時間の文字列を得る(ミリ秒)
	/// </summary>
	/// <returns>計測時間の文字列(ミリ秒)</returns>
	inline const std::string toString_ms() const { return std::to_string(millisecond()) + "ms"; }
	/// <summary>
	/// 単位付きの計測時間の文字列を得る(秒)
	/// </summary>
	/// <returns>計測時間の文字列(秒)</returns>
	inline const std::string toString_s() const { return std::to_string(second()) + "s"; }
	/// <summary>
	/// 単位付きの計測時間の文字列を得る(分)
	/// </summary>
	/// <returns>計測時間の文字列(分)</returns>
	inline const std::string toString_m() const { return std::to_string(minutes()) + "m"; }
	/// <summary>
	/// 単位付きの計測時間の文字列を得る(時)
	/// </summary>
	/// <returns>計測時間の文字列(時)</returns>
	inline const std::string toString_h() const { return std::to_string(hours()) + "h"; }

private:

	std::chrono::time_point<std::chrono::high_resolution_clock> s;
	std::chrono::time_point<std::chrono::high_resolution_clock> e;

};

class Timer {
public:

	/// <summary>
	/// コンストラクタ
	/// </summary>
	Timer() = default;
	/// <summary>
	/// コンストラクタ
	/// </summary>
	/// <param name="_time">設定時間(ナノ秒)</param>
	Timer(const std::chrono::nanoseconds& _time) { type = Type::nanoseconds; time = _time.count(); }
	/// <summary>
	/// コンストラクタ
	/// </summary>
	/// <param name="_time">設定時間(マイクロ秒)</param>
	Timer(const std::chrono::microseconds& _time) { type = Type::microseconds; time = _time.count(); }
	/// <summary>
	/// コンストラクタ
	/// </summary>
	/// <param name="_time">設定時間(ミリ秒)</param>
	Timer(const std::chrono::milliseconds& _time) { type = Type::milliseconds; time = _time.count(); }
	/// <summary>
	/// コンストラクタ
	/// </summary>
	/// <param name="_time">設定時間(秒)</param>
	Timer(const std::chrono::seconds& _time) { type = Type::seconds; time = _time.count(); }
	/// <summary>
	/// コンストラクタ
	/// </summary>
	/// <param name="_time">設定時間(分)</param>
	Timer(const std::chrono::minutes& _time) { type = Type::minutes; time = _time.count(); }
	/// <summary>
	/// コンストラクタ
	/// </summary>
	/// <param name="_time">設定時間(時)</param>
	Timer(const std::chrono::hours& _time) { type = Type::hours; time = _time.count(); }

	/// <summary>
	/// 時間を設定する
	/// </summary>
	/// <param name="_time">設定時間(ナノ秒)</param>
	void set(const std::chrono::nanoseconds& _time) { type = Type::nanoseconds; time = _time.count(); }
	/// <summary>
	/// 時間を設定する
	/// </summary>
	/// <param name="_time">設定時間(マイクロ秒)</param>
	void set(const std::chrono::microseconds& _time) { type = Type::microseconds; time = _time.count(); }
	/// <summary>
	/// 時間を設定する
	/// </summary>
	/// <param name="_time">設定時間(ミリ秒)</param>
	void set(const std::chrono::milliseconds& _time) { type = Type::milliseconds; time = _time.count(); }
	/// <summary>
	/// 時間を設定する
	/// </summary>
	/// <param name="_time">設定時間(秒)</param>
	void set(const std::chrono::seconds& _time) { type = Type::seconds; time = _time.count(); }
	/// <summary>
	/// 時間を設定する
	/// </summary>
	/// <param name="_time">設定時間(分</param>
	void set(const std::chrono::minutes& _time) { type = Type::minutes; time = _time.count(); }
	/// <summary>
	/// 時間を設定する
	/// </summary>
	/// <param name="_time">設定時間(時)</param>
	void set(const std::chrono::hours& _time) { type = Type::hours; time = _time.count(); }

	/// <summary>
	/// タイマーを開始させる
	/// </summary>
	void start() { s = std::chrono::high_resolution_clock::now(); }

	/// <summary>
	/// 設定時間経過したかを得る
	/// </summary>
	/// <returns>経過していれば true, それ以外は false</returns>
	inline const bool check() const {
		const auto e = std::chrono::high_resolution_clock::now();
		switch (type)
		{
		case Type::nanoseconds: return std::chrono::duration_cast<std::chrono::nanoseconds>(e - s).count() >= time;
		case Type::microseconds: return std::chrono::duration_cast<std::chrono::microseconds>(e - s).count() >= time;
		case Type::milliseconds: return std::chrono::duration_cast<std::chrono::milliseconds>(e - s).count() >= time;
		case Type::seconds: return std::chrono::duration_cast<std::chrono::seconds>(e - s).count() >= time;
		case Type::minutes: return std::chrono::duration_cast<std::chrono::minutes>(e - s).count() >= time;
		case Type::hours: return std::chrono::duration_cast<std::chrono::hours>(e - s).count() >= time;
		default: return true;
		}
	}

	/// <summary>
	/// 設定時間経過したかを得る
	/// </summary>
	/// <returns>経過していれば true, それ以外は false</returns>
	operator bool() const { return check(); }

private:

	enum class Type {
		nanoseconds,
		microseconds,
		milliseconds,
		seconds,
		minutes,
		hours
	};

	std::chrono::time_point<std::chrono::high_resolution_clock> s;
	long long time;
	Type type;

};

template<typename Type, size_t Width, size_t Height>
class FixedGrid {
private:

	using ContainerType = std::array<Type, Width * Height>;
	ContainerType m_data;

public:

	FixedGrid() = default;
	FixedGrid(const Type& v) { fill(v); }
	FixedGrid(const FixedGrid& other) = default;
	FixedGrid(FixedGrid&& other) {
		m_data = std::move(other.m_data);
	}

	FixedGrid& operator=(const FixedGrid& other) = default;
	FixedGrid& operator=(FixedGrid&& other) = default;

	const Type* operator[](size_t y) const {
		return &m_data[y * Width];
	}
	Type* operator[](size_t y) {
		return &m_data[y * Width];
	}
	const Type& operator[](const Point& pos) const {
		return m_data[pos.y * Width + pos.x];
	}
	Type& operator[](const Point& pos) {
		return m_data[pos.y * Width + pos.x];
	}

	const Type& at(size_t x, size_t y) const {
		if (outside(x, y))
			throw std::out_of_range("FixedGrid::at");
		return m_data[y * Width + x];
	}
	Type& at(size_t x, size_t y) {
		if (outside(x, y))
			throw std::out_of_range("FixedGrid::at");
		return m_data[y * Width + x];
	}

	constexpr size_t width() const {
		return Width;
	}
	constexpr size_t height() const {
		return Height;
	}

	bool inside(size_t x, size_t y) const {
		return (0 <= x && x < Width && 0 <= y && y < Height);
	}
	bool outside(size_t x, size_t y) const {
		return (0 > x || x >= Width || 0 > y || y >= Height);
	}

	void fill(const Type& v) noexcept {
		m_data.fill(v);
	}

	void clear() {
		m_data.swap(ContainerType());
	}

};

#pragma endregion

using Grid = FixedGrid<Cell, 24, 20>;
using Table = FixedGrid<int, 24, 20>;

#pragma region 共有データ

class Input;

class Share {
public:

	friend Input;

	static void Create() {
		instance.reset(new Share());
	}

	static Share& Get() {
		return *instance;
	}

	//以下に必要なgetterを記載

	const int Width() const { return width; }
	const int Height() const { return height; }

	/// <summary>一人の時のSAN値減少量</summary>
	const int SanityLossLonely() const { return sanityLossLonely; }
	/// <summary>二人の時のSAN値減少量</summary>
	const int SanityLossGroup() const { return sanityLossGroup; }
	/// <summary>トンべりのスポーン間隔</summary>
	const int WandererSpawnTime() const { return wandererSpawnTime; }
	/// <summary>トンべりの生存時間</summary>
	const int WandererLifeTime() const { return wandererLifeTime; }

	const Grid& getField() const { return field; }

	const Entitie getMy() const { return my; }
	const Entities getExplorers() const { return explorers; }
	const Entities getWanderers() const { return wanderers; }
	const Entities getSlashers() const { return slashers; }
	const Entities getEffectPlan() const { return effectPlan; }
	const Entities getEffectLight() const { return effectLight; }
	const Entities getEffectYell() const { return effectYell; }
	const Entities getEffectShelter() const { return effectShelter; }

	const set<int> getYell() const { return yell; }

private:

	Share() {}

	static shared_ptr<Share> instance;

	//以下に必要なデータを記載

	/// <summary>
	/// 10 ≦ w ≦ 24
	/// </summary>
	int width;
	/// <summary>
	/// 10 ≦ h ≦ 20
	/// </summary>
	int height;

	/// <summary>
	/// 0 ≦ s ≦ 8
	/// </summary>
	int spawns;
	/// <summary>
	/// 0 ≦ s ≦ 8
	/// </summary>
	int shelters;

	Grid field;

	/// <summary>
	/// <para>一人の時のSAN値減少量</para>
	/// <para>3～6</para>
	/// </summary>
	int sanityLossLonely;
	/// <summary>
	/// <para>二人の時のSAN値減少量</para>
	/// <para>1～3</para>
	/// </summary>
	int sanityLossGroup;
	/// <summary>
	/// <para>トンべりのスポーン間隔</para>
	/// <para>3～6</para>
	/// </summary>
	int wandererSpawnTime;
	/// <summary>
	/// <para>トンべりの生存時間</para>
	/// <para>30～40</para>
	/// </summary>
	int wandererLifeTime;

	Entitie my;
	Entities explorers;
	Entities wanderers;
	Entities slashers;
	Entities effectPlan;
	Entities effectLight;
	Entities effectYell;
	Entities effectShelter;

	set<int> yell;

};

shared_ptr<Share> Share::instance;

const int range(const Point& p1, const Point& p2) {
	return abs(p1.x - p2.x) + abs(p1.y - p2.y);
}

#pragma endregion

#pragma region データ入力

class Input {
private:

	set<int> minions;

public:

	Input() {}

	void first() {

		auto& share = Share::Get();

		cin >> share.width;
		cin.ignore();
		cin >> share.height;
		cin.ignore();

		for (int y = 0; y < share.height; y++)
		{
			string line;
			getline(cin, line);

			for (int x = 0; x < share.width; x++)
			{
				switch (line[x])
				{
				case Wall: share.field[y][x] = Cell::Wall; break;
				case Spawner: share.field[y][x] = Cell::Spawner; break;
				case Shelter: share.field[y][x] = Cell::Shelter; break;
				case Empty: share.field[y][x] = Cell::Empty; break;
				default:
					break;
				}
			}
		}

		cin >> share.sanityLossLonely >> share.sanityLossGroup >> share.wandererSpawnTime >> share.wandererLifeTime;
		cin.ignore();

	}

	void loop() {

		auto& share = Share::Get();

		share.explorers.clear();
		share.wanderers.clear();
		const auto bSlashers = share.slashers;
		share.slashers.clear();
		share.effectPlan.clear();
		share.effectLight.clear();
		share.effectYell.clear();
		share.effectShelter.clear();

		int entityCount;
		cin >> entityCount;
		cin.ignore();

		{
			string entityType;
			Entitie e;
			cin >> entityType >> e.id >> e.pos.x >> e.pos.y >> e.param0 >> e.param1 >> e.param2;
			cin.ignore();

			share.my = e;
		}

		for (int i = 1; i < entityCount; i++)
		{
			string entityType;
			Entitie e;
			cin >> entityType >> e.id >> e.pos.x >> e.pos.y >> e.param0 >> e.param1 >> e.param2;
			cin.ignore();

			if (entityType == Object::EXPLORER)
			{
				if (minions.find(e.id) == minions.end())
				{
					minions.insert(e.id);
					e.count = 5;
				}
				share.explorers.push_back(move(e));
			}
			else if (entityType == Object::WANDERER)
			{
				if (minions.find(e.id) == minions.end())
				{
					minions.insert(e.id);
					e.count = 6;
				}
				share.wanderers.push_back(move(e));
			}
			else if (entityType == Object::SLASHER)
			{
				for (const auto& s : bSlashers)
				{
					if (s.id == e.id)
					{
						e.nextPos = s.nextPos;
					}
				}

				share.slashers.push_back(move(e));
			}
			else if (entityType == Object::EFFECT_PLAN)
			{
				share.effectPlan.push_back(move(e));
			}
			else if (entityType == Object::EFFECT_LIGHT)
			{
				share.effectLight.push_back(move(e));
			}
			else if (entityType == Object::EFFECT_YELL)
			{
				if (range(share.my.pos, e.pos) <= 1) share.yell.insert(e.param2);
				share.effectYell.push_back(move(e));
			}
			else if (entityType == Object::EFFECT_SHELTER)
			{
				share.effectShelter.push_back(move(e));
			}

		}
	}

};

#pragma endregion

#pragma region ユーティリティ

const Point Up = Point(0, -1);
const Point Down = Point(0, 1);
const Point Right = Point(1, 0);
const Point Left = Point(-1, 0);
const Point Stay = Point(0, 0);

const Point Direction[] = { Left,Up,Right,Down,Stay };
const Point WandererDirection[] = { Up,Right,Down,Left };

const string format() {
	return "";
}

namespace Command {

	const string Move(const Point& pos) {
		return "MOVE " + to_string(pos.x) + " " + to_string(pos.y);
	}
	const string Wait() {
		return "WAIT";
	}


	/// <summary>
	/// <para>回復ゾーンを展開する</para>
	/// <para>5ターン有効でほかプレイヤーの近くにいるとSAN値を3回復する</para>
	/// <para>2回まで使用可能</para>
	/// </summary>
	/// <returns></returns>
	const string Plan() {
		return "PLAN";
	}

	/// <summary>
	/// <para>防御ゾーンを展開する</para>
	/// <para>3ターン有効で距離5マス以内のセルに経路コストを4増やす</para>
	/// <para>3回まで使用可能</para>
	/// </summary>
	/// <returns></returns>
	const string Light() {
		return "LIGHT";
	}

	/// <summary>
	/// <para>ほかプレイヤーを拘束する</para>
	/// <para>距離が1以下のプレイヤーを2ターンその場に拘束する</para>
	/// <para>1プレイヤーに対して1回のみ</para>
	/// <para>使用回数は不定？</para>
	/// </summary>
	/// <returns></returns>
	const string Yell() {
		return "YELL";
	}
}

#pragma endregion

#pragma region AI

constexpr int Turn = 5;
constexpr int ChokudaiWidth = 3;

struct Data {

	Entitie my;
	Entities explorers;

	Entities wanderers;
	Entities slashers;

	Entities effectPlan;
	Entities effectLight;
	Entities effectYell;

	Entities effectShelter;

	array<pair<int, Point>, Turn> commands;

	int eval;

	bool operator<(const Data& other) const {
		return eval < other.eval;
	}

};

class Simulator {
private:

	Table makeCostTable(const Entities& effectLight) {

		Table table(Inf);

		for (int y = 0; y < h; y++)
		{
			for (int x = 0; x < w; x++)
			{
				if (field[y][x] != Cell::Wall)
				{
					table[y][x] = 1;
				}
			}
		}

		const int EffectRange = 5;
		const int Cost = 4;

		for (const auto& effect : effectLight)
		{
			if (effect.param0 > 0)
			{
				queue<Point> que;
				Table check(0);

				que.push(effect.pos);
				table[effect.pos] += Cost;
				check[effect.pos] = 1;

				for (int i = 0; i < EffectRange; i++)
				{
					queue<Point> next;
					while (!que.empty())
					{
						for (const auto& dire : Direction)
						{
							const auto& pos = que.front() + dire;
							if (table[pos] != Inf && check[pos] == 0)
							{
								table[pos] += Cost;
								check[pos] = 1;
								next.push(pos);
							}
						}
						que.pop();
					}
					que.swap(next);
				}
			}
		}

		return table;
	}

	Table makeHealTable(const Entities& effectPlan) {

		Table table(0);

		const int EffectRange = 2;
		const int Add = 3;

		for (const auto& effect : effectPlan)
		{
			if (effect.param0 > 0)
			{
				queue<Point> que;
				Table check(0);

				que.push(effect.pos);
				table[effect.pos] += Add;
				check[effect.pos] = 1;

				for (int i = 0; i < EffectRange; i++)
				{
					queue<Point> next;
					while (!que.empty())
					{
						for (const auto& dire : Direction)
						{
							const auto& pos = que.front() + dire;
							if (field[pos] != Cell::Wall && check[pos] == 0)
							{
								table[pos] += Add;
								check[pos] = 1;
								next.push(pos);
							}
						}
						que.pop();
					}
					que.swap(next);
				}
			}
		}

		return table;
	}

	Table makeRangeTable(const Entitie& my, const Entities& explorers, const Table& costTable, const Entities& effectLight) {

		Table table(Inf);

		const int size = (int)effectLight.size();
		if (size > 0)
		{
			const int index = size * 1000 + effectLight.front().id;
			if (rangeTableCache.find(index) == rangeTableCache.end())
			{
				for (const auto& e : explorers)
				{
					updateRangeTable(e, costTable, table);
				}
				rangeTableCache[index] = table;
			}
			else
			{
				table = rangeTableCache[index];
			}
		}

		updateRangeTable(my, costTable, table);

		return table;
	}

	map<int, Table> rangeTableCache;

	void updateRangeTable(const Entitie& e, const Table& cost, Table& table) {

		queue<Point> que;
		que.push(e.pos);
		table[e.pos] = 0;

		while (!que.empty())
		{
			queue<Point> next;

			while (!que.empty())
			{
				const auto& front = que.front();
				const int r = table[front];

				for (const auto& dire : Direction)
				{
					const auto& pos = front + dire;

					if (table[pos] > r + cost[pos])
					{
						table[pos] = r + cost[pos];
						next.emplace(pos);
					}
				}

				que.pop();
			}

			que.swap(next);
		}

	}

	void updateMinion(Data& next) {

		const auto& costTable = makeCostTable(next.effectLight);
		const auto& rangeTable = makeRangeTable(next.my, next.explorers, costTable, next.effectLight);

		{
			if (next.my.param0 <= 200 && next.my.count > 200)
			{
				Entitie e;
				e.id = 5000 + (int)next.slashers.size();
				e.pos = e.pos;
				e.param0 = 6;
				e.param1 = Object::SPAWNING;
				e.param2 = -1;
				e.count = 6;

				next.slashers.emplace_back(e);
			}
			next.my.count = next.my.param0;
		}
		for (auto& ex : next.explorers)
		{
			if (ex.param0 <= 200 && ex.count > 200)
			{
				Entitie e;
				e.id = 5000 + (int)next.slashers.size();
				e.pos = ex.pos;
				e.param0 = 6;
				e.param1 = Object::SPAWNING;
				e.param2 = -1;
				e.count = 6;

				next.slashers.emplace_back(e);
			}
			ex.count = ex.param0;
		}

		for (auto& w : next.wanderers)
		{
			w.count--;
			if (w.count <= 0)
			{
				int minR = rangeTable[w.pos];
				Point nextP;
				for (const auto& dire : WandererDirection)
				{
					const auto& pos = w.pos + dire;
					if (minR > rangeTable[pos])
					{
						minR = rangeTable[pos];
						nextP = pos;
					}
				}

				if (nextP)
					w.pos = nextP;
			}
		}

		const auto findPlayer = [&](const Entitie& my, const Entities& explorers, const Entitie& slasher) {

			{
				if (my.pos.x == slasher.pos.x)
				{
					int start = min(my.pos.x, slasher.pos.x) + 1;
					int end = max(my.pos.x, slasher.pos.x);

					bool find = true;
					for (int i = start; i < end; i++)
					{
						if (field[slasher.pos.y][i] == Cell::Wall)
						{
							find = false;
							break;
						}
					}
					if (find)
						return my.pos;
				}
				else if (my.pos.y == slasher.pos.y)
				{
					int start = min(my.pos.y, slasher.pos.y) + 1;
					int end = max(my.pos.y, slasher.pos.y);

					bool find = true;
					for (int i = start; i < end; i++)
					{
						if (field[i][slasher.pos.x] == Cell::Wall)
						{
							find = false;
							break;
						}
					}
					if (find)
						return my.pos;
				}
			}

			for (const auto& e : explorers)
			{
				if (e.pos.x == slasher.pos.x)
				{
					int start = min(e.pos.x, slasher.pos.x) + 1;
					int end = max(e.pos.x, slasher.pos.x);

					bool find = true;
					for (int i = start; i < end; i++)
					{
						if (field[slasher.pos.y][i] == Cell::Wall)
						{
							find = false;
							break;
						}
					}
					if (find)
						return e.pos;
				}
				else if (e.pos.y == slasher.pos.y)
				{
					int start = min(e.pos.y, slasher.pos.y) + 1;
					int end = max(e.pos.y, slasher.pos.y);

					bool find = true;
					for (int i = start; i < end; i++)
					{
						if (field[i][slasher.pos.x] == Cell::Wall)
						{
							find = false;
							break;
						}
					}
					if (find)
						return e.pos;
				}
			}

			return Point();
		};

		for (auto& s : next.slashers)
		{
			switch (s.param1)
			{
			case Object::SPAWNING:
				s.count--;
				if (s.count <= 0)
				{
					const auto pos = findPlayer(next.my, next.explorers, s);
					if (pos)
					{
						s.nextPos = pos;
						s.param1 = Object::RUSHING;
					}
					else
						s.param1 = Object::WANDERING;

				}
				break;
			case Object::WANDERING:
			{
				int minR = rangeTable[s.pos];
				Point nextP;
				for (const auto& dire : WandererDirection)
				{
					const auto& pos = s.pos + dire;
					if (minR > rangeTable[pos])
					{
						minR = rangeTable[pos];
						nextP = pos;
					}
				}
				if (nextP)
					s.pos = nextP;

				const auto pos = findPlayer(next.my, next.explorers, s);
				if (pos)
				{
					s.param1 = Object::STALKING;
					s.nextPos = pos;
					s.count = 2;
				}
			}
			break;
			case Object::STALKING:
			{
				s.count--;
				if (s.count <= 0)
				{
					s.param1 = Object::STALKING;
					const auto pos = findPlayer(next.my, next.explorers, s);
					if (pos)
					{
						s.nextPos = pos;
						s.param1 = Object::RUSHING;
					}
				}
			}
			break;
			case Object::RUSHING:
			{
				const auto pos = findPlayer(next.my, next.explorers, s);
				if (pos) s.nextPos = pos;
				s.pos = s.nextPos;
			}
			break;
			case Object::STUNNED:
				s.count--;
				if (s.count <= 0)
				{
					const auto pos = findPlayer(next.my, next.explorers, s);
					if (pos)
					{
						s.nextPos = pos;
						s.param1 = Object::RUSHING;
					}
					else
						s.param1 = Object::WANDERING;
				}
				break;
			default:
				break;
			}
		}
	}

	void updateEntities(Data& next) {

		for (auto& e : next.effectPlan)
		{
			e.param0--;
			if (e.param1 == next.my.id)
				e.pos = next.my.pos;
		}

		for (auto& e : next.effectLight) { e.param0--; }
		for (auto& e : next.effectYell) { e.param0--; }

		const auto& healTable = makeHealTable(next.effectPlan);

		next.my.param0 += healTable[next.my.pos];
		for (auto& e : next.explorers)
			e.param0 += healTable[e.pos];

		for (auto& e : next.effectShelter)
		{
			if (e.param0 > 0)
			{
				if (next.my.pos == e.pos)
				{
					next.my.param0 += 5;
					e.param0--;
				}

				for (auto& e : next.explorers)
				{
					if (e.pos == e.pos)
					{
						e.param0 += 5;
						e.param0--;
					}
				}
			}
		}

		{
			bool near[4] = { 0 };

			for (const auto& e : next.explorers)
			{
				if (range(next.my.pos, e.pos) < 2)
				{
					near[next.my.id] = true;
					near[e.id] = true;
				}
			}

			const int size = (int)next.explorers.size();
			for (int i = 0; i < size - 1; i++)
			{
				for (int j = i + 1; j < size; j++)
				{
					if (range(next.explorers[i].pos, next.explorers[j].pos) <= 2)
					{
						near[next.explorers[i].id] = true;
						near[next.explorers[j].id] = true;
					}
				}
			}

			next.my.param0 -= near[next.my.id] ? sanityLossGroup : sanityLossLonely;

			for (auto& e : next.explorers)
			{
				e.param0 -= near[e.id] ? sanityLossGroup : sanityLossLonely;
			}
		}

		for (auto& w : next.wanderers)
		{
			if (next.my.pos == w.pos)
			{
				next.my.param0 -= 20;
				w.param0 = 0;
			}

			for (auto& e : next.explorers)
			{
				if (e.pos == w.pos)
				{
					e.param0 -= 20;
					w.param0 = 0;
				}
			}

		}
		for (auto& s : next.slashers)
		{
			if (s.param1 == Object::RUSHING)
			{
				if (next.my.pos == s.pos)
				{
					next.my.param0 -= 20;
				}
				for (auto& e : next.explorers)
				{
					if (e.pos == s.pos)
					{
						e.param0 -= 20;
					}
				}
				s.param1 = Object::STUNNED;
				s.count = 6;
			}
		}

		for (auto it = next.explorers.begin(); it != next.explorers.end();)
		{
			if (it->param0 > 0) ++it;
			else it = next.explorers.erase(it);
		}
		for (auto it = next.wanderers.begin(); it != next.wanderers.end();)
		{
			if (it->param0 > 0) ++it;
			else it = next.wanderers.erase(it);
		}
		for (auto it = next.explorers.begin(); it != next.explorers.end();)
		{
			if (it->param0 > 0) ++it;
			else it = next.explorers.erase(it);
		}

	}

	int getScore(const Data& next) {

		int score = 0;

		array<int, 4> explorersRange;
		explorersRange.fill(5000);

		for (const auto& e : next.explorers)
			explorersRange[e.id] = range(next.my.pos, e.pos);

		//0 - 250
		const int hp = next.my.param0;

		//0 - 250
		const int minHp = [&]() {
			int m = 300;
			for (const auto& e : next.explorers)
				m = min(m, e.param0);
			return m;
		}();
		//0 - 750
		const int sumHp = [&]() {
			int sum = 0;
			for (const auto& e : next.explorers)
				sum += e.param0;
			return sum;
		}();

		//0 - 3
		const int near = [&]() {
			int count = 0;
			for (const auto& r : explorersRange)
				if (r < 2) count++;
			return count;
		}();

		const int plan = next.my.param1;
		const int light = next.my.param2;

		int canMove = 100;

		for (int id = 1; id < 4; id++)
		{
			if (explorersRange[id] <= 1)
			{
				if (yell.find(id) == yell.end())
				{
					canMove /= 2;
				}
			}
		}

		int slasherCount = 0;

		for (const auto& s : next.slashers)
		{
			if (next.my.pos.x == s.pos.x)
			{
				int start = min(next.my.pos.x, s.pos.x) + 1;
				int end = max(next.my.pos.x, s.pos.x);

				bool find = true;
				for (int i = start; i < end; i++)
				{
					if (field[s.pos.y][i] == Cell::Wall)
					{
						find = false;
						break;
					}
				}
				if (find)
					slasherCount++;
			}
			else if (next.my.pos.y == s.pos.y)
			{
				int start = min(next.my.pos.y, s.pos.y) + 1;
				int end = max(next.my.pos.y, s.pos.y);

				bool find = true;
				for (int i = start; i < end; i++)
				{
					if (field[i][s.pos.x] == Cell::Wall)
					{
						find = false;
						break;
					}
				}
				if (find)
					slasherCount++;
			}
		}

		score += hp * 100;
		score -= sumHp * 20;
		//score -= minHp;

		//score += near * 10;
		//score -= min({ explorersRange[0],explorersRange[1],explorersRange[2] }) * 10;

		score += plan * 200;
		score += light;

		//score += canMove * 100;

		score -= slasherCount * 20 * 100;

		return score;
	}

	const Grid& field;
	const int w;
	const int h;
	const int sanityLossLonely;
	const int sanityLossGroup;

public:

	set<int> yell;

	Simulator(const Grid& _field, const int _w, const int _h, const int lossLonely, const int lossGroup)
		: field(_field), w(_w), h(_h), sanityLossLonely(lossLonely), sanityLossGroup(lossGroup) {}

	void next(const Data& top, priority_queue<Data>& qData, int turn) {

		rangeTableCache.clear();

		//TODO: Yell
		//TODO: プレイヤー移動

		const auto& pos = top.my.pos;

		const auto& plan = top.my.param1;
		const auto& light = top.my.param2;

		const auto update = [&](Data&& next) {

			updateMinion(next);

			updateEntities(next);

			//if (next.my.param0 > 0)
			{
				next.eval = getScore(next);

				qData.emplace(next);
			}
		};

		if (plan > 0 && top.my.param0 < 210)
		{
			auto next = top;

			next.my.param1--;

			next.commands[turn].first = 1;
			next.commands[turn].second = next.my.pos;

			Entitie e;

			e.id = 1000 + (int)next.effectPlan.size();
			e.pos = next.my.pos;
			e.param0 = 5;
			e.param1 = next.my.id;
			e.param2 = -1;

			next.effectPlan.emplace_back(e);

			update(move(next));
		}

		if (light > 0)
		{
			auto next = top;

			next.my.param2--;

			next.commands[turn].first = 2;
			next.commands[turn].second = next.my.pos;

			Entitie e;

			e.id = 1000 + (int)next.effectLight.size();
			e.pos = next.my.pos;
			e.param0 = 3;
			e.param1 = next.my.id;
			e.param2 = -1;

			next.effectLight.emplace_back(e);

			update(move(next));
		}

		for (const auto& dire : Direction)
		{
			const auto nextPos = pos + dire;

			if (field[nextPos] != Cell::Wall)
			{
				auto next = top;

				next.my.pos = nextPos;

				next.commands[turn].first = 0;
				next.commands[turn].second = next.my.pos;

				update(move(next));
			}
		}

	}

};

class AI {
public:

	vector<string> think() {

		const auto& share = Share::Get();

		const auto& field = share.getField();

		const auto& sanityLossLonely = share.SanityLossLonely();
		const auto& sanityLossGroup = share.SanityLossGroup();
		const auto& wandererSpawnTime = share.WandererSpawnTime();
		const auto& wandererLifeTime = share.WandererLifeTime();

		array<priority_queue<Data>, Turn + 1> qData;
		{
			Data now;

			now.my = share.getMy();
			now.explorers = share.getExplorers();

			now.my.count = now.my.param0;
			for (auto& e : now.explorers) e.count = e.param0;

			now.wanderers = share.getWanderers();
			now.slashers = share.getSlashers();

			now.effectPlan = share.getEffectPlan();
			now.effectLight = share.getEffectLight();;
			now.effectYell = share.getEffectYell();

			now.effectShelter = share.getEffectShelter();;

			now.eval = 0;

			qData[0].emplace(now);
		}

		Simulator simulator(share.getField(), share.Width(), share.Height(), share.SanityLossLonely(), share.SanityLossGroup());
		simulator.yell = share.getYell();

		Timer timer(chrono::milliseconds(45));

		timer.start();

		while (!timer)
		{
			for (int turn = 0; turn < Turn; turn++)
			{
				for (int w = 0; w < ChokudaiWidth; w++)
				{
					if (qData[turn].empty())
						break;

					const auto& top = qData[turn].top();

					simulator.next(top, qData[turn + 1], turn);

					qData[turn].pop();

				}
			}

		}

		if (!qData[Turn].empty())
		{
			cerr << "Score:" << qData[Turn].top().eval << endl;
			cerr << "HP:" << qData[Turn].top().my.param0 << endl;

			const auto& top = qData[Turn].top();

			vector<string> coms;

			if (top.commands[0].first == 0)
				coms.push_back(Command::Move(top.commands[0].second));
			else if (top.commands[0].first == 1)
				coms.push_back(Command::Plan());
			else
				coms.push_back(Command::Light());

			const auto d = [](const Point& p1, const Point& p2) {

				const auto dp = p2 - p1;

				if (dp == Up) return "U";
				if (dp == Down) return "D";
				if (dp == Right) return "R";
				if (dp == Left) return "L";
				return "S";
			};

			string nextMove = "";
			for (int i = 0; i < 4; i++) nextMove += d(top.commands[i].second, top.commands[i + 1].second);
			coms.push_back(nextMove);

			return coms;
		}

		cerr << "詰みです" << endl;
		return { "WAIT","詰みです(´・ω・`)" };
	}

};

#pragma endregion

#pragma region データ出力

int main() {

	Share::Create();

	Input input;
	input.first();

	Stopwatch sw;

	AI ai;

	while (true)
	{
		input.loop();

		sw.start();
		const auto& coms = ai.think();
		sw.stop();

		cerr << sw.toString_ms() << endl;

		string command = "";
		for (const auto& com : coms)
		{
			command += com + " ";
		}
		command.pop_back();

		cout << command << endl;

	}

	return 0;
}

#pragma endregion