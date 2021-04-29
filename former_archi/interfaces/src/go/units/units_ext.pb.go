// Code generated by protoc-gen-go. DO NOT EDIT.
// source: units/units_ext.proto

package units

import (
	fmt "fmt"
	proto "github.com/golang/protobuf/proto"
	descriptor "github.com/golang/protobuf/protoc-gen-go/descriptor"
	math "math"
)

// Reference imports to suppress errors if they are not otherwise used.
var _ = proto.Marshal
var _ = fmt.Errorf
var _ = math.Inf

// This is a compile-time assertion to ensure that this generated file
// is compatible with the proto package it is being compiled against.
// A compilation error at this line likely means your copy of the
// proto package needs to be updated.
const _ = proto.ProtoPackageIsVersion3 // please upgrade the proto package

var E_DefaultDegrees = &proto.ExtensionDesc{
	ExtendedType:  (*descriptor.FieldOptions)(nil),
	ExtensionType: (*Degrees)(nil),
	Field:         60002,
	Name:          "units.default_degrees",
	Tag:           "bytes,60002,opt,name=default_degrees",
	Filename:      "units/units_ext.proto",
}

var E_MinDegrees = &proto.ExtensionDesc{
	ExtendedType:  (*descriptor.FieldOptions)(nil),
	ExtensionType: (*Degrees)(nil),
	Field:         60003,
	Name:          "units.min_degrees",
	Tag:           "bytes,60003,opt,name=min_degrees",
	Filename:      "units/units_ext.proto",
}

var E_MaxDegrees = &proto.ExtensionDesc{
	ExtendedType:  (*descriptor.FieldOptions)(nil),
	ExtensionType: (*Degrees)(nil),
	Field:         60004,
	Name:          "units.max_degrees",
	Tag:           "bytes,60004,opt,name=max_degrees",
	Filename:      "units/units_ext.proto",
}

var E_DefaultMeters = &proto.ExtensionDesc{
	ExtendedType:  (*descriptor.FieldOptions)(nil),
	ExtensionType: (*Meters)(nil),
	Field:         60005,
	Name:          "units.default_meters",
	Tag:           "bytes,60005,opt,name=default_meters",
	Filename:      "units/units_ext.proto",
}

var E_MinMeters = &proto.ExtensionDesc{
	ExtendedType:  (*descriptor.FieldOptions)(nil),
	ExtensionType: (*Meters)(nil),
	Field:         60006,
	Name:          "units.min_meters",
	Tag:           "bytes,60006,opt,name=min_meters",
	Filename:      "units/units_ext.proto",
}

var E_MaxMeters = &proto.ExtensionDesc{
	ExtendedType:  (*descriptor.FieldOptions)(nil),
	ExtensionType: (*Meters)(nil),
	Field:         60007,
	Name:          "units.max_meters",
	Tag:           "bytes,60007,opt,name=max_meters",
	Filename:      "units/units_ext.proto",
}

var E_DefaultMetersPerSecond = &proto.ExtensionDesc{
	ExtendedType:  (*descriptor.FieldOptions)(nil),
	ExtensionType: (*MetersPerSecond)(nil),
	Field:         60008,
	Name:          "units.default_meters_per_second",
	Tag:           "bytes,60008,opt,name=default_meters_per_second",
	Filename:      "units/units_ext.proto",
}

var E_MinMetersPerSecond = &proto.ExtensionDesc{
	ExtendedType:  (*descriptor.FieldOptions)(nil),
	ExtensionType: (*MetersPerSecond)(nil),
	Field:         60009,
	Name:          "units.min_meters_per_second",
	Tag:           "bytes,60009,opt,name=min_meters_per_second",
	Filename:      "units/units_ext.proto",
}

var E_MaxMetersPerSecond = &proto.ExtensionDesc{
	ExtendedType:  (*descriptor.FieldOptions)(nil),
	ExtensionType: (*MetersPerSecond)(nil),
	Field:         60010,
	Name:          "units.max_meters_per_second",
	Tag:           "bytes,60010,opt,name=max_meters_per_second",
	Filename:      "units/units_ext.proto",
}

var E_DefaultPascals = &proto.ExtensionDesc{
	ExtendedType:  (*descriptor.FieldOptions)(nil),
	ExtensionType: (*Pascals)(nil),
	Field:         60011,
	Name:          "units.default_pascals",
	Tag:           "bytes,60011,opt,name=default_pascals",
	Filename:      "units/units_ext.proto",
}

var E_MinPascals = &proto.ExtensionDesc{
	ExtendedType:  (*descriptor.FieldOptions)(nil),
	ExtensionType: (*Pascals)(nil),
	Field:         60012,
	Name:          "units.min_pascals",
	Tag:           "bytes,60012,opt,name=min_pascals",
	Filename:      "units/units_ext.proto",
}

var E_MaxPascals = &proto.ExtensionDesc{
	ExtendedType:  (*descriptor.FieldOptions)(nil),
	ExtensionType: (*Pascals)(nil),
	Field:         60013,
	Name:          "units.max_pascals",
	Tag:           "bytes,60013,opt,name=max_pascals",
	Filename:      "units/units_ext.proto",
}

var E_DefaultCelsius = &proto.ExtensionDesc{
	ExtendedType:  (*descriptor.FieldOptions)(nil),
	ExtensionType: (*Celsius)(nil),
	Field:         60014,
	Name:          "units.default_celsius",
	Tag:           "bytes,60014,opt,name=default_celsius",
	Filename:      "units/units_ext.proto",
}

var E_MinCelsius = &proto.ExtensionDesc{
	ExtendedType:  (*descriptor.FieldOptions)(nil),
	ExtensionType: (*Celsius)(nil),
	Field:         60015,
	Name:          "units.min_celsius",
	Tag:           "bytes,60015,opt,name=min_celsius",
	Filename:      "units/units_ext.proto",
}

var E_MaxCelsius = &proto.ExtensionDesc{
	ExtendedType:  (*descriptor.FieldOptions)(nil),
	ExtensionType: (*Celsius)(nil),
	Field:         60016,
	Name:          "units.max_celsius",
	Tag:           "bytes,60016,opt,name=max_celsius",
	Filename:      "units/units_ext.proto",
}

var E_DefaultMetersPerSecondSquared = &proto.ExtensionDesc{
	ExtendedType:  (*descriptor.FieldOptions)(nil),
	ExtensionType: (*MetersPerSecondSquared)(nil),
	Field:         60020,
	Name:          "units.default_meters_per_second_squared",
	Tag:           "bytes,60020,opt,name=default_meters_per_second_squared",
	Filename:      "units/units_ext.proto",
}

var E_MinMetersPerSecondSquared = &proto.ExtensionDesc{
	ExtendedType:  (*descriptor.FieldOptions)(nil),
	ExtensionType: (*MetersPerSecondSquared)(nil),
	Field:         60021,
	Name:          "units.min_meters_per_second_squared",
	Tag:           "bytes,60021,opt,name=min_meters_per_second_squared",
	Filename:      "units/units_ext.proto",
}

var E_MaxMetersPerSecondSquared = &proto.ExtensionDesc{
	ExtendedType:  (*descriptor.FieldOptions)(nil),
	ExtensionType: (*MetersPerSecondSquared)(nil),
	Field:         60022,
	Name:          "units.max_meters_per_second_squared",
	Tag:           "bytes,60022,opt,name=max_meters_per_second_squared",
	Filename:      "units/units_ext.proto",
}

func init() {
	proto.RegisterExtension(E_DefaultDegrees)
	proto.RegisterExtension(E_MinDegrees)
	proto.RegisterExtension(E_MaxDegrees)
	proto.RegisterExtension(E_DefaultMeters)
	proto.RegisterExtension(E_MinMeters)
	proto.RegisterExtension(E_MaxMeters)
	proto.RegisterExtension(E_DefaultMetersPerSecond)
	proto.RegisterExtension(E_MinMetersPerSecond)
	proto.RegisterExtension(E_MaxMetersPerSecond)
	proto.RegisterExtension(E_DefaultPascals)
	proto.RegisterExtension(E_MinPascals)
	proto.RegisterExtension(E_MaxPascals)
	proto.RegisterExtension(E_DefaultCelsius)
	proto.RegisterExtension(E_MinCelsius)
	proto.RegisterExtension(E_MaxCelsius)
	proto.RegisterExtension(E_DefaultMetersPerSecondSquared)
	proto.RegisterExtension(E_MinMetersPerSecondSquared)
	proto.RegisterExtension(E_MaxMetersPerSecondSquared)
}

func init() { proto.RegisterFile("units/units_ext.proto", fileDescriptor_160a8e706d42bcab) }

var fileDescriptor_160a8e706d42bcab = []byte{
	// 480 bytes of a gzipped FileDescriptorProto
	0x1f, 0x8b, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0xff, 0x94, 0xd5, 0x5f, 0xab, 0xd3, 0x30,
	0x14, 0x00, 0x70, 0x86, 0x28, 0x98, 0xcb, 0xbd, 0xe2, 0xe0, 0x5e, 0xbc, 0x17, 0x0a, 0xf3, 0x4d,
	0x11, 0x5a, 0xd0, 0xb7, 0x3e, 0xaa, 0xf8, 0x36, 0x1c, 0x1d, 0x82, 0xf8, 0x52, 0xb2, 0xf6, 0xac,
	0x46, 0xda, 0xa6, 0x26, 0x29, 0xe4, 0xd1, 0x47, 0x3f, 0xa0, 0x9f, 0xc0, 0xff, 0xff, 0xf5, 0x41,
	0x7d, 0x96, 0x35, 0x49, 0xd7, 0x6e, 0x0d, 0xcd, 0x5e, 0x06, 0x49, 0x76, 0x7e, 0xe7, 0xe4, 0x2c,
	0x87, 0xa1, 0xd3, 0xba, 0x24, 0x82, 0x07, 0xcd, 0x67, 0x0c, 0x52, 0xf8, 0x15, 0xa3, 0x82, 0x4e,
	0x2f, 0x37, 0x1b, 0x17, 0xb3, 0x8c, 0xd2, 0x2c, 0x87, 0xa0, 0xd9, 0x5c, 0xd5, 0xeb, 0x20, 0x05,
	0x9e, 0x30, 0x52, 0x09, 0xca, 0xd4, 0x17, 0x2f, 0xae, 0x77, 0xe2, 0xd5, 0x56, 0xf8, 0x14, 0x5d,
	0x4b, 0x61, 0x8d, 0xeb, 0x5c, 0xc4, 0x29, 0x64, 0x0c, 0x80, 0x4f, 0x3d, 0x5f, 0x41, 0xbe, 0x81,
	0xfc, 0x47, 0x04, 0xf2, 0xf4, 0x71, 0x25, 0x08, 0x2d, 0xf9, 0x8d, 0xb7, 0x6f, 0x2e, 0xcd, 0x26,
	0xb7, 0x8e, 0xee, 0x9e, 0xf8, 0xca, 0x79, 0xa8, 0xc2, 0xa2, 0x13, 0xed, 0xe8, 0x75, 0xb8, 0x40,
	0x47, 0x05, 0x29, 0x5d, 0xd5, 0x77, 0x16, 0x15, 0x15, 0xa4, 0xec, 0x8a, 0x58, 0xba, 0x8a, 0xef,
	0xad, 0x22, 0x96, 0x46, 0x7c, 0x82, 0x4c, 0xd5, 0x71, 0x01, 0x02, 0xd8, 0x28, 0xfa, 0x41, 0xa3,
	0xc7, 0x1a, 0x9d, 0x37, 0x51, 0xd1, 0xb1, 0x56, 0xd4, 0x32, 0x9c, 0xa3, 0x4d, 0xd9, 0x8e, 0xe4,
	0xc7, 0x61, 0xf2, 0x6a, 0x41, 0xca, 0x0e, 0x87, 0xa5, 0x23, 0xf7, 0xc9, 0xc6, 0x61, 0xa9, 0x39,
	0x86, 0xce, 0xfb, 0x97, 0x8e, 0x2b, 0x60, 0x31, 0x87, 0x84, 0x96, 0xe9, 0x98, 0xfe, 0x59, 0xeb,
	0x67, 0x3d, 0x7d, 0x01, 0x6c, 0xd9, 0x84, 0x47, 0x67, 0xbd, 0x46, 0xb4, 0xfb, 0xe1, 0x0b, 0x74,
	0xba, 0xed, 0xc8, 0x01, 0xf9, 0xbe, 0x8c, 0xe4, 0x9b, 0xb6, 0x5d, 0xea, 0xe7, 0x6a, 0xdb, 0x75,
	0x40, 0xae, 0xaf, 0xa3, 0xb9, 0x4c, 0x0b, 0xb7, 0xb9, 0x3a, 0xe3, 0x53, 0x61, 0x9e, 0xe0, 0x7c,
	0xf4, 0xf7, 0xf9, 0xb6, 0xf3, 0x2c, 0x17, 0x2a, 0xac, 0x1d, 0x1f, 0xbd, 0x36, 0xe3, 0xe3, 0xa8,
	0x7e, 0xb7, 0xa8, 0x9b, 0x77, 0xd8, 0x15, 0xb1, 0x74, 0x15, 0x7f, 0x58, 0x45, 0x2c, 0x8d, 0xd8,
	0xb9, 0x7d, 0x02, 0x39, 0x27, 0xf5, 0xa8, 0xfa, 0x73, 0x47, 0x7d, 0xa0, 0xc2, 0xda, 0xdb, 0xeb,
	0xb5, 0xb9, 0xbd, 0xa3, 0xfa, 0xcb, 0xa2, 0x6e, 0x6e, 0xdf, 0x15, 0xb1, 0x74, 0x15, 0x7f, 0x5b,
	0x45, 0x2c, 0x8d, 0xf8, 0x7a, 0x82, 0x6e, 0x5a, 0x07, 0x29, 0xe6, 0x2f, 0x6b, 0xcc, 0x60, 0xf4,
	0xd1, 0xfd, 0xd1, 0x89, 0xbc, 0xe1, 0x47, 0xb7, 0x54, 0x4a, 0xe4, 0x0d, 0xcf, 0x95, 0x3e, 0x0e,
	0x5f, 0x4d, 0x90, 0x37, 0x38, 0x5f, 0xae, 0x65, 0xfc, 0x75, 0x2b, 0xe3, 0x7c, 0x7f, 0xdc, 0x7a,
	0x25, 0x0c, 0x8d, 0x9d, 0x6b, 0x09, 0xff, 0x5c, 0x4b, 0xd8, 0x9b, 0x42, 0x7d, 0x74, 0xff, 0xce,
	0xb3, 0xdb, 0x19, 0x11, 0xcf, 0xeb, 0x95, 0x9f, 0xd0, 0x22, 0xc0, 0x84, 0x15, 0xb8, 0x0a, 0x48,
	0x29, 0x80, 0xad, 0x71, 0x02, 0x3c, 0xe0, 0x2c, 0x09, 0x32, 0xaa, 0xfe, 0xfe, 0x56, 0x57, 0x9a,
	0x2a, 0xee, 0xfd, 0x0f, 0x00, 0x00, 0xff, 0xff, 0x50, 0xf9, 0x22, 0x7f, 0x54, 0x07, 0x00, 0x00,
}